"""HTTP route tests for the interface settings, key manager, and user guide."""

import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import Interface.server as server_module
from Interface.server import create_server
from Interface.utils import settings


SYSTEM = {
	"system_name": "Route Mock System",
	"architecture_target": "Microservices",
	"requirements": "Manage records.",
	"reference_services": "Record Service",
	"reference_interactions": "Record -> Audit",
}

MOCK_RUN = {
	"ok": True,
	"run_id": "mock-run",
	"metrics": {
		"proposta_a": {"precision": 0.9, "recall": 0.8, "f1_score": 0.85},
		"proposta_b": {"precision": 0.8, "recall": 0.9, "f1_score": 0.85},
		"consolidada": {"precision": 0.88, "recall": 0.86, "f1_score": 0.87},
	},
	"results": {
		"proposta_a": "Microservice,Responsibilities,Communicates With\nA,Manage A,B",
		"proposta_b": "Microservice,Responsibilities,Communicates With\nB,Manage B,A",
		"consolidada": "Microservice,Responsibilities,Communicates With\nA,Manage A,B",
	},
}


class SettingsRouteTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.temporary = tempfile.TemporaryDirectory()
		cls.root = Path(cls.temporary.name)
		cls.env_path = cls.root / ".env"
		cls.settings_path = cls.root / "settings.json"
		cls.env_path.write_text(
			"DEEPSEEK_API_KEY=deepseek-existing\nGOOGLE_API_KEY=gemini-existing\n",
			encoding="utf-8",
		)
		cls.patchers = [
			patch.object(settings, "ENV_PATH", cls.env_path),
			patch.object(settings, "SETTINGS_PATH", cls.settings_path),
			patch.object(server_module, "RESULTS_DIR", cls.root / "result"),
		]
		for patcher in cls.patchers:
			patcher.start()
		server_module.LATEST_RUN = None
		cls.server = create_server(port=0)
		cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
		cls.thread.start()
		cls.base = f"http://127.0.0.1:{cls.server.server_port}"

	@classmethod
	def tearDownClass(cls):
		cls.server.shutdown()
		cls.server.server_close()
		for patcher in cls.patchers:
			patcher.stop()
		cls.temporary.cleanup()

	def get_raw(self, path):
		return urlopen(self.base + path).read()

	def get_json(self, path):
		return json.loads(self.get_raw(path))

	def post_json(self, path, payload):
		request = Request(
			self.base + path,
			data=json.dumps(payload).encode(),
			headers={"Content-Type": "application/json"},
		)
		with urlopen(request) as response:
			return response.status, response.read()

	def post_json_error(self, path, payload):
		request = Request(
			self.base + path,
			data=json.dumps(payload).encode(),
			headers={"Content-Type": "application/json"},
		)
		with self.assertRaises(HTTPError) as context:
			urlopen(request)
		return context.exception.code, json.loads(context.exception.read())

	def env_text(self):
		return self.env_path.read_text(encoding="utf-8")

	def test_settings_payload_lists_every_configuration_and_provider(self):
		payload = self.get_json("/api/settings")
		self.assertTrue(payload["ok"])
		self.assertEqual([item["id"] for item in payload["configurations"]], ["c0", "c1", "c2", "c3", "c4", "c5"])
		self.assertEqual([item["id"] for item in payload["providers"]], ["deepseek", "gemini", "claude"])
		deepseek = next(item for item in payload["providers"] if item["id"] == "deepseek")
		self.assertTrue(deepseek["configured"])
		self.assertEqual(deepseek["model"], "deepseek-chat")
		self.assertIn(1, [key["number"] for key in deepseek["keys"]])
		self.assertTrue(any(key["active"] for key in deepseek["keys"]))
		self.assertNotIn("deepseek-existing", json.dumps(payload))
		self.assertNotIn("gemini-existing", json.dumps(payload))

	def test_configuration_and_provider_are_persisted(self):
		status, body = self.post_json("/api/settings", {"configuration": "c4", "provider": "gemini"})
		self.assertEqual(status, 200)
		payload = json.loads(body)
		self.assertEqual(payload["configuration"], "c4")
		self.assertEqual(payload["provider"], "gemini")
		again = self.get_json("/api/settings")
		self.assertEqual((again["configuration"], again["provider"]), ("c4", "gemini"))
		self.assertEqual(settings.load_settings()["configuration"], "c4")

	def test_invalid_configuration_and_provider_are_rejected(self):
		code, payload = self.post_json_error("/api/settings", {"configuration": "c9"})
		self.assertEqual(code, 400)
		self.assertEqual(payload["code"], "invalid_configuration")
		code, payload = self.post_json_error("/api/settings", {"provider": "openai"})
		self.assertEqual(code, 400)
		self.assertEqual(payload["code"], "invalid_provider")

	def test_key_selection_requires_a_provider_and_a_registered_key(self):
		code, payload = self.post_json_error("/api/settings", {"key_number": 1})
		self.assertEqual(code, 400)
		self.assertEqual(payload["code"], "provider_required")
		code, payload = self.post_json_error("/api/settings", {"provider": "deepseek", "key_number": 9})
		self.assertEqual(code, 400)
		self.assertEqual(payload["code"], "key_not_found")

	def test_new_key_is_saved_without_being_returned(self):
		secret = "sk-route-secret-value-123"
		status, body = self.post_json("/api/settings/api-key", {"provider": "gemini", "key": secret})
		self.assertEqual(status, 200)
		payload = json.loads(body)
		self.assertTrue(payload["ok"])
		self.assertEqual(payload["saved_key"], {"number": 2, "label": "Key 2", "active": False})
		self.assertNotIn(secret, body.decode("utf-8"))
		self.assertIn(f"# GOOGLE_API_KEY_2={secret}", self.env_text())
		self.assertNotIn(secret, self.settings_path.read_text(encoding="utf-8"))
		keys = next(item for item in payload["providers"] if item["id"] == "gemini")["keys"]
		self.assertEqual([key["label"] for key in keys], ["Key 1", "Key 2"])
		self.assertNotIn(secret, json.dumps(self.get_json("/api/settings")))

	def test_activating_a_saved_key_rewrites_the_active_line(self):
		secret = "sk-route-active-value"
		status, body = self.post_json(
			"/api/settings/api-key",
			{"provider": "deepseek", "key": secret, "make_active": True},
		)
		self.assertEqual(status, 200)
		payload = json.loads(body)
		self.assertEqual(payload["saved_key"]["number"], 2)
		self.assertTrue(payload["saved_key"]["active"])
		text = self.env_text()
		self.assertIn(f"DEEPSEEK_API_KEY={secret}", text)
		self.assertIn("# DEEPSEEK_API_KEY_1=deepseek-existing", text)
		self.assertNotIn(secret, body.decode("utf-8"))
		self.assertEqual(settings.active_key_value("deepseek"), secret)

	def test_invalid_key_requests_are_rejected(self):
		code, payload = self.post_json_error("/api/settings/api-key", {"provider": "openai", "key": "x"})
		self.assertEqual((code, payload["code"]), (400, "invalid_provider"))
		code, payload = self.post_json_error("/api/settings/api-key", {"provider": "deepseek", "key": "  "})
		self.assertEqual((code, payload["code"]), (400, "empty_key"))
		code, payload = self.post_json_error(
			"/api/settings/api-key",
			{"provider": "deepseek", "key": "x", "make_active": "yes"},
		)
		self.assertEqual((code, payload["code"]), (400, "invalid_option"))

	def test_user_guide_is_served_in_english(self):
		response = urlopen(self.base + "/user-guide")
		body = response.read()
		self.assertEqual(response.status, 200)
		self.assertEqual(response.headers.get_content_type(), "text/html")
		for marker in (b"USER GUIDE", b"C0", b"C5", b"DeepSeek", b"Gemini", b"Claude", b"SAVE KEY"):
			self.assertIn(marker, body)

	def test_unknown_mode_is_rejected(self):
		code, payload = self.post_json_error(
			"/api/pipeline/run",
			{"systems": [{**SYSTEM, "mode": "c9"}]},
		)
		self.assertEqual((code, payload["code"]), (400, "invalid_mode"))
		code, payload = self.post_json_error(
			"/api/pipeline/run",
			{"systems": [{**SYSTEM, "mode": 3}]},
		)
		self.assertEqual((code, payload["code"]), (400, "invalid_mode"))

	def test_provider_without_key_blocks_the_run(self):
		code, payload = self.post_json_error(
			"/api/pipeline/run",
			{"systems": [{**SYSTEM, "mode": "c1"}], "provider": "claude"},
		)
		self.assertEqual((code, payload["code"]), (400, "provider_key_missing"))

	def test_mocked_run_uses_the_selected_mode_and_provider(self):
		captured = {}

		def fake_pipeline(system, tracer_run_id=None):
			captured["mode"] = system.get("mode")
			captured["provider"] = os.environ.get("DAVINCI_LLM_PROVIDER")
			captured["google_key"] = os.environ.get("GOOGLE_API_KEY")
			return MOCK_RUN

		with patch.dict(os.environ, {}, clear=False), \
				patch.object(server_module, "run_real_pipeline", side_effect=fake_pipeline):
			status, body = self.post_json(
				"/api/pipeline/run",
				{"systems": [{**SYSTEM, "mode": "c3"}], "provider": "gemini"},
			)
		payload = json.loads(body)
		self.assertEqual(status, 200)
		self.assertTrue(payload["ok"])
		self.assertEqual(captured["mode"], "c3")
		self.assertEqual(captured["provider"], "gemini")
		self.assertEqual(captured["google_key"], "gemini-existing")
		self.assertEqual(payload["configuration"], "c3")
		self.assertEqual(payload["configuration_label"], "C3")
		self.assertEqual(payload["provider"], "gemini")
		self.assertEqual(payload["ai_label"], "Gemini (gemini-flash-latest)")
		self.assertEqual(payload["model"], "gemini-flash-latest")
		self.assertEqual(payload["key_label"], "Key 1")
		self.assertNotIn("gemini-existing", body.decode("utf-8"))


if __name__ == "__main__":
	unittest.main()
