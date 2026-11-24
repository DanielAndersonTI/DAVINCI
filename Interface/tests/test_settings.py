"""Unit tests for server-side settings and the `.env` key manager."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Interface.utils import settings


class SettingsTestCase(unittest.TestCase):
	def setUp(self):
		self.temporary = tempfile.TemporaryDirectory()
		self.root = Path(self.temporary.name)
		self.env_path = self.root / ".env"
		self.settings_path = self.root / "settings.json"
		self.patchers = [
			patch.object(settings, "ENV_PATH", self.env_path),
			patch.object(settings, "SETTINGS_PATH", self.settings_path),
		]
		for patcher in self.patchers:
			patcher.start()

	def tearDown(self):
		for patcher in self.patchers:
			patcher.stop()
		self.temporary.cleanup()

	def write_env(self, *lines):
		self.env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

	def env_text(self):
		return self.env_path.read_text(encoding="utf-8")


class DefaultSettingsTests(SettingsTestCase):
	def test_missing_file_falls_back_to_defaults(self):
		current = settings.load_settings()
		self.assertEqual(current["configuration"], "c1")
		self.assertEqual(current["provider"], "deepseek")

	def test_corrupt_file_falls_back_to_defaults(self):
		self.settings_path.write_text("{not json", encoding="utf-8")
		self.assertEqual(settings.load_settings()["configuration"], "c1")

	def test_save_is_atomic_and_has_no_temporary_file(self):
		settings.set_configuration("c3")
		self.assertTrue(self.settings_path.is_file())
		self.assertFalse(self.settings_path.with_name("settings.json.tmp").exists())

	def test_failed_replace_keeps_previous_content(self):
		settings.set_configuration("c2")
		previous = self.settings_path.read_text(encoding="utf-8")
		with patch.object(settings.os, "replace", side_effect=OSError("locked")):
			with self.assertRaises(OSError):
				settings.set_configuration("c4")
		self.assertEqual(self.settings_path.read_text(encoding="utf-8"), previous)


class SelectionTests(SettingsTestCase):
	def test_configuration_validation_and_persistence(self):
		self.assertEqual(settings.set_configuration("C3"), "c3")
		self.assertEqual(settings.load_settings()["configuration"], "c3")
		with self.assertRaises(settings.SettingsError):
			settings.set_configuration("c9")

	def test_provider_validation_and_persistence(self):
		self.assertEqual(settings.set_provider("Gemini"), "gemini")
		self.assertEqual(settings.load_settings()["provider"], "gemini")
		with self.assertRaises(settings.SettingsError):
			settings.set_provider("openai")


class KeyManagerTests(SettingsTestCase):
	def test_existing_plain_key_is_key_one(self):
		self.write_env("DEEPSEEK_API_KEY=sk-old")
		keys = settings.public_keys("deepseek")
		self.assertEqual(keys, [{"number": 1, "label": "Key 1", "active": True}])
		self.assertEqual(settings.active_key_value("deepseek"), "sk-old")

	def test_new_key_is_appended_and_previous_stays(self):
		self.write_env("DEEPSEEK_API_KEY=sk-old")
		number, active = settings.add_key("deepseek", "sk-new", make_active=False)
		self.assertEqual((number, active), (2, False))
		text = self.env_text()
		self.assertIn("DEEPSEEK_API_KEY=sk-old", text)
		self.assertIn("# DEEPSEEK_API_KEY_2=sk-new", text)
		self.assertEqual(settings.active_key_value("deepseek"), "sk-old")
		self.assertEqual([key["number"] for key in settings.public_keys("deepseek")], [1, 2])

	def test_activating_a_new_key_comments_the_previous_one(self):
		self.write_env("DEEPSEEK_API_KEY=sk-old")
		settings.add_key("deepseek", "sk-new", make_active=False)
		number, active = settings.add_key("deepseek", "sk-third", make_active=True)
		self.assertEqual((number, active), (3, True))
		text = self.env_text()
		self.assertIn("# DEEPSEEK_API_KEY_1=sk-old", text)
		self.assertIn("# DEEPSEEK_API_KEY_2=sk-new", text)
		self.assertIn("DEEPSEEK_API_KEY=sk-third", text)
		self.assertEqual(settings.active_key_value("deepseek"), "sk-third")

	def test_selecting_a_registered_key_rewrites_the_active_line(self):
		self.write_env("DEEPSEEK_API_KEY=sk-old")
		settings.add_key("deepseek", "sk-new", make_active=False)
		settings.select_key("deepseek", 2)
		text = self.env_text()
		self.assertIn("DEEPSEEK_API_KEY=sk-new", text)
		self.assertIn("# DEEPSEEK_API_KEY_1=sk-old", text)
		self.assertEqual(settings.active_key_value("deepseek"), "sk-new")
		self.assertEqual(settings.load_settings()["active_key"]["deepseek"], 2)

	def test_selecting_an_unknown_key_is_rejected(self):
		self.write_env("DEEPSEEK_API_KEY=sk-old")
		with self.assertRaises(settings.SettingsError) as context:
			settings.select_key("deepseek", 7)
		self.assertEqual(context.exception.code, "key_not_found")

	def test_empty_and_multiline_keys_are_rejected(self):
		with self.assertRaises(settings.SettingsError):
			settings.add_key("deepseek", "   ")
		with self.assertRaises(settings.SettingsError):
			settings.add_key("deepseek", "line1\nline2")

	def test_first_key_for_an_unconfigured_provider_becomes_active(self):
		number, active = settings.add_key("claude", "sk-claude", make_active=False)
		self.assertEqual((number, active), (1, True))
		self.assertEqual(settings.active_key_value("claude"), "sk-claude")

	def test_key_values_never_reach_the_settings_payload(self):
		self.write_env("DEEPSEEK_API_KEY=sk-secret-value")
		settings.add_key("gemini", "gemini-secret-value", make_active=True)
		payload = json.dumps(settings.settings_payload())
		self.assertNotIn("sk-secret-value", payload)
		self.assertNotIn("gemini-secret-value", payload)
		self.assertNotIn("sk-secret-value", self.settings_path.read_text(encoding="utf-8"))


class EnvironmentTests(SettingsTestCase):
	def test_provider_environment_is_applied_from_the_env_file(self):
		self.write_env("GOOGLE_API_KEY=google-secret", "GOOGLE_MODEL=custom-gemini")
		with patch.dict(os.environ, {}, clear=False):
			os.environ.pop("DAVINCI_LLM_PROVIDER", None)
			applied = settings.apply_provider_environment("gemini")
			self.assertEqual(os.environ["DAVINCI_LLM_PROVIDER"], "gemini")
			self.assertEqual(os.environ["GOOGLE_API_KEY"], "google-secret")
			self.assertEqual(os.environ["GEMINI_API_KEY"], "google-secret")
		self.assertEqual(applied["model"], "custom-gemini")
		self.assertEqual(applied["label"], "Gemini")

	def test_provider_without_key_is_rejected_before_running(self):
		with self.assertRaises(settings.SettingsError) as context:
			settings.apply_provider_environment("claude")
		self.assertEqual(context.exception.code, "provider_key_missing")

	def test_provider_model_uses_the_documented_default(self):
		self.assertEqual(settings.provider_model("deepseek"), "deepseek-chat")
		self.assertEqual(settings.provider_model("claude"), "claude-sonnet-4-5-20250929")


if __name__ == "__main__":
	unittest.main()
