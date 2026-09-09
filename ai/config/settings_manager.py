import json
from copy import deepcopy
from pathlib import Path
from typing import Any




BASE_DIR = Path(__file__).parent

DEFAULT_SETTINGS = {
    "telegram": {
        "token": "",
        "bot_trigger_name": "",
        "default_prompt": "",
    },
    "ai": {
        "custom_models": [],
        "providers": {
            "openai": {
                "api_key": "",
                "base_url": "https://api.openai.com/v1",
            },
            "groq": {
                "api_key": "",
                "base_url": "https://api.groq.com/openai/v1",
            },
            "openrouter": {
                "api_key": "",
                "base_url": "https://openrouter.ai/api/v1",
            },
        },
    },
}


class SettingsManager:

    def __init__(self, path: str = "settings.json") -> None:
        self.path = Path(BASE_DIR / path)
        self._settings: dict[str, Any] = {}
        self.load()


    def load(self) -> None:
        if not self.path.exists():
            self._settings = deepcopy(DEFAULT_SETTINGS)
            self.save()
            return

        with self.path.open("r", encoding="utf-8") as file:
            self._settings = json.load(file)


    def save(self) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                self._settings,
                file,
                indent=4,
                ensure_ascii=False,
            )


    def get(self, key: str, default: Any = None) -> Any:
        current = self._settings

        for part in key.split("."):
            if not isinstance(current, dict):
                return default

            if part not in current:
                return default

            current = current[part]

        return current

    def set(self, key: str, value: Any) -> None:
        parts = key.split(".")

        current = self._settings
    
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
    
            current = current[part]
    
        current[parts[-1]] = value
    
        self.save()