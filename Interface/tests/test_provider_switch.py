"""Provider switching must leave no stale provider behind.

The interface, the settings file, the `.env` file and the LLM factory are four
places that have to agree. These tests cycle DeepSeek, Gemini and Claude through
the real selection functions and assert what `criar_llm()` would build.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dotenv import dotenv_values

from Interface.utils import settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = PROJECT_ROOT / "Experimento_Multiagente"
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

import main_fewshot  # noqa: E402  (path is prepared above)


ENV_CONTENT = "\n".join([
    "DAVINCI_LLM_PROVIDER=gemini",
    "DEEPSEEK_API_KEY=sk-deepseek",
    "DEEPSEEK_MODEL=deepseek-chat",
    "GOOGLE_API_KEY=google-key",
    "GOOGLE_MODEL=gemini-flash-latest",
    "ANTHROPIC_API_KEY=anthropic-key",
    "CLAUDE_MODEL=claude-sonnet-4-5-20250929",
])


class FakeLLM:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.model = kwargs.get("model")


class ProviderSwitchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.env_path = self.root / ".env"
        self.env_path.write_text(ENV_CONTENT + "\n", encoding="utf-8")
        self.settings_path = self.root / "settings.json"

        def load_temp_env(path=None, *args, **kwargs):
            """Emulate load_dotenv(override=False) against the isolated .env."""
            for name, value in dotenv_values(self.env_path).items():
                if value is not None:
                    os.environ.setdefault(name, value)
            return True

        self.patchers = [
            patch.object(settings, "ENV_PATH", self.env_path),
            patch.object(settings, "SETTINGS_PATH", self.settings_path),
            patch.dict(os.environ, {}, clear=False),
            patch.object(main_fewshot, "load_dotenv", new=load_temp_env),
            patch.object(main_fewshot, "_apply_ca_bundle", new=lambda: None),
        ]
        for patcher in self.patchers:
            patcher.start()
        os.environ.pop("DAVINCI_LLM_PROVIDER", None)
        for name in ("DEEPSEEK_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY"):
            os.environ.pop(name, None)

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temporary.cleanup()

    def env_text(self):
        return self.env_path.read_text(encoding="utf-8")

    def test_each_ui_provider_reaches_the_llm_factory(self):
        expected = {
            "deepseek": ("deepseek/", "sk-deepseek"),
            "gemini": ("gemini/", "google-key"),
            "claude": ("anthropic/", "anthropic-key"),
        }
        with patch.object(main_fewshot, "LLM", new=lambda **kwargs: FakeLLM(**kwargs)):
            for ui_provider, (prefix, key) in expected.items():
                with self.subTest(provider=ui_provider):
                    applied = settings.apply_provider_environment(ui_provider)
                    llm = main_fewshot.criar_llm()
                    self.assertEqual(applied["provider"], ui_provider)
                    self.assertTrue(llm.model.startswith(prefix), llm.model)
                    self.assertEqual(llm.kwargs["api_key"], key)

    def test_ui_selection_rewrites_the_env_provider(self):
        self.assertIn("DAVINCI_LLM_PROVIDER=gemini", self.env_text())
        settings.set_provider("deepseek")
        text = self.env_text()
        self.assertIn("DAVINCI_LLM_PROVIDER=deepseek", text)
        self.assertNotIn("DAVINCI_LLM_PROVIDER=gemini", text)
        self.assertEqual(os.environ["DAVINCI_LLM_PROVIDER"], "deepseek")

    def test_standalone_factory_uses_the_last_ui_selection(self):
        settings.set_provider("claude")
        # Simulate a script started later, with no provider in the environment.
        os.environ.pop("DAVINCI_LLM_PROVIDER", None)
        with patch.object(main_fewshot, "LLM", new=lambda **kwargs: FakeLLM(**kwargs)):
            llm = main_fewshot.criar_llm()
        self.assertTrue(llm.model.startswith("anthropic/"), llm.model)
        self.assertEqual(llm.kwargs["api_key"], "anthropic-key")

    def test_server_start_applies_the_saved_provider(self):
        settings.set_provider("gemini")
        os.environ.pop("DAVINCI_LLM_PROVIDER", None)
        with patch.object(settings, "load_settings", return_value={**settings.default_settings(), "provider": "claude"}):
            self.assertEqual(settings.sync_provider_environment(), "claude")
        self.assertEqual(os.environ["DAVINCI_LLM_PROVIDER"], "anthropic")


if __name__ == "__main__":
    unittest.main()
