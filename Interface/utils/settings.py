"""Server-side settings and API key management for the DAVINCI interface.

The settings file stores only non-secret preferences. API keys live in the
project `.env` file, which is ignored by Git. Key values are never returned to
the browser and never written to logs or reports.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from threading import Lock
from typing import Any

INTERFACE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = INTERFACE_DIR.parent
SETTINGS_PATH = INTERFACE_DIR / "settings.json"
ENV_PATH = PROJECT_ROOT / "Experimento_Multiagente" / ".env"

CONFIGURATIONS = ("c0", "c1", "c2", "c3", "c4", "c5")
DEFAULT_CONFIGURATION = "c1"

CONFIGURATION_DETAILS = {
    "c0": {
        "label": "C0 - Single proposal",
        "description": "Agent 1 only. One architecture, no second proposal, no refinement, no consolidation, no YAML export stage.",
    },
    "c1": {
        "label": "C1 - Complete pipeline",
        "description": "Agents 1, 2, 4, 3 and 5. Two proposals, refinement, consolidation and the YAML specification. This is the reference configuration.",
    },
    "c2": {
        "label": "C2 - No refinement",
        "description": "Agents 1, 2, 3 and 5. The complete pipeline without Agent 4, which isolates the contribution of the refinement stage.",
    },
    "c3": {
        "label": "C3 - Single refined proposal",
        "description": "Agents 1, 4 and 5. Agent 2 and Agent 3 are removed together: one proposal is refined and exported.",
    },
    "c4": {
        "label": "C4 - Generalist second proposal",
        "description": "Agents 1, 2.1, 4, 3 and 5. Agent 2 is replaced by Agent 2.1, a generalist with the same prompt as Agent 1 and a different example.",
    },
    "c5": {
        "label": "C5 - Consolidator control",
        "description": "Control condition for Agent 3. Without a frozen run directory it regenerates the proposals like C1 and runs Agent 3 twice, so it costs more.",
    },
}

PROVIDERS: dict[str, dict[str, Any]] = {
    "deepseek": {
        "label": "DeepSeek",
        "key_var": "DEEPSEEK_API_KEY",
        "model_var": "DEEPSEEK_MODEL",
        "default_model": "deepseek-chat",
        "provider_env": "deepseek",
        "env_vars": ("DEEPSEEK_API_KEY",),
    },
    "gemini": {
        "label": "Gemini",
        "key_var": "GOOGLE_API_KEY",
        "model_var": "GOOGLE_MODEL",
        "default_model": "gemini-flash-latest",
        "provider_env": "gemini",
        "env_vars": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    },
    "claude": {
        "label": "Claude",
        "key_var": "ANTHROPIC_API_KEY",
        "model_var": "CLAUDE_MODEL",
        "default_model": "claude-sonnet-4-5-20250929",
        "provider_env": "anthropic",
        "env_vars": ("ANTHROPIC_API_KEY",),
    },
}
DEFAULT_PROVIDER = "deepseek"

_ENV_LINE = re.compile(r"^\s*(#\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")
_SETTINGS_LOCK = Lock()


class SettingsError(Exception):
    """Raised when a settings or key operation is rejected."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def default_settings() -> dict[str, Any]:
    return {
        "configuration": DEFAULT_CONFIGURATION,
        "provider": DEFAULT_PROVIDER,
        "active_key": {provider: 1 for provider in PROVIDERS},
    }


def _normalize_settings(raw: Any) -> dict[str, Any]:
    settings = default_settings()
    if not isinstance(raw, dict):
        return settings
    configuration = str(raw.get("configuration", "")).strip().lower()
    if configuration in CONFIGURATIONS:
        settings["configuration"] = configuration
    provider = str(raw.get("provider", "")).strip().lower()
    if provider in PROVIDERS:
        settings["provider"] = provider
    active_key = raw.get("active_key")
    if isinstance(active_key, dict):
        for provider_id in PROVIDERS:
            number = active_key.get(provider_id)
            if isinstance(number, int) and not isinstance(number, bool) and number >= 1:
                settings["active_key"][provider_id] = number
    return settings


def load_settings() -> dict[str, Any]:
    try:
        raw = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default_settings()
    return _normalize_settings(raw)


def save_settings(settings: dict[str, Any]) -> dict[str, Any]:
    normalized = _normalize_settings(settings)
    payload = json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
    with _SETTINGS_LOCK:
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary = SETTINGS_PATH.with_name(SETTINGS_PATH.name + ".tmp")
        temporary.write_text(payload, encoding="utf-8", newline="\n")
        os.replace(temporary, SETTINGS_PATH)
    return normalized


def set_configuration(configuration: str) -> str:
    mode = str(configuration).strip().lower()
    if mode not in CONFIGURATIONS:
        raise SettingsError("invalid_configuration", f"Unknown configuration: {configuration}.")
    settings = load_settings()
    settings["configuration"] = mode
    save_settings(settings)
    return mode


def set_provider(provider: str) -> str:
    provider_id = str(provider).strip().lower()
    if provider_id not in PROVIDERS:
        raise SettingsError("invalid_provider", f"Unknown AI provider: {provider}.")
    settings = load_settings()
    settings["provider"] = provider_id
    save_settings(settings)
    # The interface, the pipeline factory and standalone scripts must all read
    # the same provider. settings.json alone is not enough: criar_llm() reads
    # the process environment, which load_dotenv() fills from .env. Updating
    # both here removes the stale provider that used to survive a switch.
    _set_env_var("DAVINCI_LLM_PROVIDER", PROVIDERS[provider_id]["provider_env"], create=True)
    os.environ["DAVINCI_LLM_PROVIDER"] = PROVIDERS[provider_id]["provider_env"]
    return provider_id


def sync_provider_environment() -> str:
    """Apply the saved provider to the process environment at server start.

    A run request without an explicit provider (for example when the browser
    could not load /api/settings) then still uses the saved selection instead
    of whatever value happened to be in the environment.
    """
    provider_id = load_settings()["provider"]
    os.environ["DAVINCI_LLM_PROVIDER"] = PROVIDERS[provider_id]["provider_env"]
    return provider_id


def set_active_key(provider: str, number: int) -> dict[str, Any]:
    provider_id = _require_provider(provider)
    number = _require_key_number(number)
    settings = load_settings()
    settings["active_key"][provider_id] = number
    return save_settings(settings)


def _require_provider(provider: str) -> str:
    provider_id = str(provider).strip().lower()
    if provider_id not in PROVIDERS:
        raise SettingsError("invalid_provider", f"Unknown AI provider: {provider}.")
    return provider_id


def _require_key_number(number: Any) -> int:
    if isinstance(number, bool) or not isinstance(number, int) or number < 1:
        raise SettingsError("invalid_key_number", "The key number must be a positive integer.")
    return number


def _strip_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _env_entries(lines: list[str]):
    for index, line in enumerate(lines):
        match = _ENV_LINE.match(line)
        if not match:
            continue
        yield index, bool(match.group(1)), match.group(2), _strip_value(match.group(3))


def _read_env_lines() -> list[str]:
    try:
        return ENV_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def _write_env_lines(lines: list[str]) -> None:
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines).rstrip("\n") + "\n"
    with _SETTINGS_LOCK:
        temporary = ENV_PATH.with_name(ENV_PATH.name + ".tmp")
        temporary.write_text(content, encoding="utf-8", newline="\n")
        os.replace(temporary, ENV_PATH)


def _set_env_var(name: str, value: str, create: bool) -> None:
    """Pin a non-secret variable to one value in the `.env` file.

    Every uncommented occurrence is rewritten so a duplicated line cannot keep
    the previous value. With `create` false a missing file is left untouched.
    """
    if not create and not ENV_PATH.exists():
        return
    lines = _read_env_lines()
    changed = False
    found = False
    for index, commented, entry_name, entry_value in _env_entries(lines):
        if commented or entry_name != name:
            continue
        found = True
        if entry_value != value:
            lines[index] = f"{name}={value}"
            changed = True
    if not found:
        lines.append(f"{name}={value}")
        changed = True
    if changed:
        _write_env_lines(lines)


def _file_var(name: str) -> str | None:
    value = None
    for _, commented, entry_name, entry_value in _env_entries(_read_env_lines()):
        if not commented and entry_name == name:
            value = entry_value
    return value


def _active_entry(provider_id: str, lines: list[str]) -> tuple[int, str, str] | None:
    provider = PROVIDERS[provider_id]
    found = None
    for index, commented, name, value in _env_entries(lines):
        if commented or name not in provider["env_vars"]:
            continue
        if value:
            found = (index, name, value)
    return found


def _numbered_entries(provider_id: str, lines: list[str]) -> dict[int, tuple[int, bool, str]]:
    prefix = PROVIDERS[provider_id]["key_var"] + "_"
    entries: dict[int, tuple[int, bool, str]] = {}
    for index, commented, name, value in _env_entries(lines):
        if not name.startswith(prefix):
            continue
        suffix = name[len(prefix):]
        if suffix.isdigit() and value:
            entries[int(suffix)] = (index, commented, value)
    return entries


def active_key_value(provider_id: str) -> str | None:
    provider_id = _require_provider(provider_id)
    entry = _active_entry(provider_id, _read_env_lines())
    return entry[2] if entry else None


def _active_key_number(provider_id: str, lines: list[str], settings: dict[str, Any]) -> int | None:
    if _active_entry(provider_id, lines) is None:
        return None
    stored = settings.get("active_key", {}).get(provider_id)
    if isinstance(stored, int) and not isinstance(stored, bool) and stored >= 1:
        return stored
    numbered = _numbered_entries(provider_id, lines)
    return next(iter(numbered), 1)


def public_keys(provider_id: str, settings: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    provider_id = _require_provider(provider_id)
    settings = settings or load_settings()
    lines = _read_env_lines()
    numbered = _numbered_entries(provider_id, lines)
    active_number = _active_key_number(provider_id, lines, settings)
    numbers = set(numbered)
    if active_number is not None:
        numbers.add(active_number)
    return [
        {"number": number, "label": f"Key {number}", "active": number == active_number}
        for number in sorted(numbers)
    ]


def provider_configured(provider_id: str) -> bool:
    return active_key_value(provider_id) is not None


def provider_model(provider_id: str) -> str:
    provider = PROVIDERS[_require_provider(provider_id)]
    value = _file_var(provider["model_var"])
    if value:
        return value
    return provider["default_model"]


def settings_payload() -> dict[str, Any]:
    settings = load_settings()
    providers = []
    for provider_id, provider in PROVIDERS.items():
        providers.append({
            "id": provider_id,
            "label": provider["label"],
            "model": provider_model(provider_id),
            "configured": provider_configured(provider_id),
            "keys": public_keys(provider_id, settings),
        })
    return {
        "ok": True,
        "configuration": settings["configuration"],
        "provider": settings["provider"],
        "key_number": settings["active_key"].get(settings["provider"]),
        "configurations": [
            {"id": mode, **CONFIGURATION_DETAILS[mode]}
            for mode in CONFIGURATIONS
        ],
        "providers": providers,
    }


def add_key(provider: str, key: str, make_active: bool = False) -> tuple[int, bool]:
    """Register a new key for a provider.

    Returns the key number and whether it became the active key. The key value is
    written only to the `.env` file.
    """
    provider_id = _require_provider(provider)
    value = str(key or "").strip()
    if not value:
        raise SettingsError("empty_key", "Enter an API key before saving.")
    if any(character in value for character in "\r\n"):
        raise SettingsError("invalid_key", "The API key must be a single line.")

    provider_cfg = PROVIDERS[provider_id]
    key_var = provider_cfg["key_var"]
    lines = _read_env_lines()
    settings = load_settings()
    numbered = _numbered_entries(provider_id, lines)
    active_entry = _active_entry(provider_id, lines)
    active_number = _active_key_number(provider_id, lines, settings)

    existing_numbers = set(numbered)
    if active_number is not None:
        existing_numbers.add(active_number)
    number = max(existing_numbers, default=0) + 1

    activate = bool(make_active) or active_entry is None
    if activate and active_entry is not None:
        old_index = active_entry[0]
        old_number = active_number or 1
        old_value = active_entry[2]
        lines[old_index] = f"# {key_var}_{old_number}={old_value}"
        duplicate = numbered.get(old_number)
        if duplicate is not None and duplicate[0] != old_index:
            del lines[duplicate[0]]

    if activate:
        lines.append(f"{key_var}={value}")
        os.environ[key_var] = value
        if provider_id == "gemini":
            os.environ["GEMINI_API_KEY"] = value
        settings["active_key"][provider_id] = number
        save_settings(settings)
    else:
        lines.append(f"# {key_var}_{number}={value}")

    _write_env_lines(lines)
    return number, activate


def select_key(provider: str, number: int) -> dict[str, Any]:
    provider_id = _require_provider(provider)
    number = _require_key_number(number)
    lines = _read_env_lines()
    settings = load_settings()
    numbered = _numbered_entries(provider_id, lines)
    active_entry = _active_entry(provider_id, lines)
    active_number = _active_key_number(provider_id, lines, settings)

    if number == active_number:
        settings["active_key"][provider_id] = number
        return save_settings(settings)
    if number not in numbered:
        raise SettingsError("key_not_found", f"Key {number} is not registered for {PROVIDERS[provider_id]['label']}.")

    _, _, target_value = numbered[number]
    key_var = PROVIDERS[provider_id]["key_var"]
    if active_entry is not None:
        old_index = active_entry[0]
        old_number = active_number or 1
        old_value = active_entry[2]
        lines[old_index] = f"# {key_var}_{old_number}={old_value}"
        duplicate = numbered.get(old_number)
        if duplicate is not None and duplicate[0] != old_index:
            del lines[duplicate[0]]
    target_index = _numbered_entries(provider_id, lines)[number][0]
    lines[target_index] = f"{key_var}={target_value}"
    _write_env_lines(lines)

    os.environ[key_var] = target_value
    if provider_id == "gemini":
        os.environ["GEMINI_API_KEY"] = target_value
    settings["active_key"][provider_id] = number
    return save_settings(settings)


def apply_provider_environment(provider: str) -> dict[str, str]:
    """Apply the selected provider and its active key to the process environment."""
    provider_id = _require_provider(provider)
    value = active_key_value(provider_id)
    if not value:
        label = PROVIDERS[provider_id]["label"]
        raise SettingsError(
            "provider_key_missing",
            f"No API key is configured for {label}. Add a key in the interface before running the pipeline.",
        )
    provider_cfg = PROVIDERS[provider_id]
    os.environ["DAVINCI_LLM_PROVIDER"] = provider_cfg["provider_env"]
    os.environ[provider_cfg["key_var"]] = value
    if provider_id == "gemini":
        os.environ["GEMINI_API_KEY"] = value
    # Keep .env truthful even when the run payload carried a provider that was
    # not saved through the settings endpoint. The write is skipped when the
    # value already matches, so the normal run does not touch the file.
    _set_env_var("DAVINCI_LLM_PROVIDER", provider_cfg["provider_env"], create=False)
    return {
        "provider": provider_id,
        "label": provider_cfg["label"],
        "model": provider_model(provider_id),
    }


def provider_label(provider: str) -> str:
    return PROVIDERS[_require_provider(provider)]["label"]


def ai_label(provider: str) -> str:
    provider_id = _require_provider(provider)
    return f"{PROVIDERS[provider_id]['label']} ({provider_model(provider_id)})"
