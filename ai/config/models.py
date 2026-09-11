from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal



@dataclass
class ModelConfig:
    name: str
    model_id: str
    provider: str
    builtin: bool = False
    free: bool = False



class ModelRegistry(QObject):
    models_changed = Signal()

    def __init__(self, settings):
        super().__init__()
        self.models: list[ModelConfig] = []
        self.settings = settings

        self._load_custom_models()
        self._register_builtin_models()


    def get_models(self) -> list[ModelConfig]:
        return self.models.copy()


    def get_available_models(self):
        providers = self.settings.get("ai.providers")
        connected_providers = [provider for provider
                                in providers
                                if providers[provider].get("api_key", "")]

        return [model for model
                in self.models 
                if model.provider in connected_providers]


    def get_model_by_name(self, name) -> ModelConfig:
        for model in self.models:
            if name == model.name:
                return model


    def _register_builtin_models(self):
        self.register_model(
            name="openai_gpt5.6_luna",
            model_id="gpt-5.6-luna",
            provider="openai"
        )

        self.register_model(
            name="groq_qwen3.6",
            model_id="qwen/qwen3.6-27b",
            provider="groq"
        )

        self.register_model(
            name="groq_gpt-oss",
            model_id="openai/gpt-oss-120b",
            provider="groq"
        )

        self.register_model(
            name="groq_gpt-oss-mini",
            model_id="openai/gpt-oss-20b",
            provider="groq"
        )

        self.register_model(
            name="openrouter_liquid/lfm-2.5-2.6b",
            model_id="liquid/lfm-2.5-2.6b:free",
            provider="openrouter"
        )

        self.register_model(
            name="openrouter_/glm-5.2",
            model_id="z-ai/glm-5.2:free",
            provider="openrouter"
        )

        self.register_model(
            name="openrouter_minimax-m3",
            model_id="minimax/minimax-m3:free",
            provider="openrouter"
        )


    def register_model(
        self,
        name: str,
        model_id: str,
        provider: str,
        free: bool = True,
    ) -> None:
        
        self.models.append(
            ModelConfig(
                name=name,
                model_id=model_id,
                provider=provider,
                free=free,
                builtin=True,
            )
        )


    def _load_custom_models(self) -> None:
        custom_models = self.settings.get(
            "ai.custom_models"
        ) or []

        for model in custom_models:
            self.models.append(
                ModelConfig(
                    name=model["name"],
                    model_id=model["model_id"],
                    provider=model["provider"],
                    free=model.get("is_free", False),
                    builtin=False,
                )
            )


    def add_custom_model(
        self,
        name: str,
        model_id: str,
        provider: str,
        free: bool = False,
    ) -> None:

        if any(model.name == name for model in self.models):
            raise ValueError(
                f"Модель с именем '{name}' уже существует"
            )

        model = ModelConfig(
            name=name,
            model_id=model_id,
            provider=provider,
            free=free,
            builtin=False,
        )

        self.models.append(model)

        custom_models = self.settings.get(
            "ai.custom_models"
        ) or []

        custom_models.append({
            "name": name,
            "model_id": model_id,
            "provider": provider,
            "is_free": free,
        })

        self.settings.set(
            "ai.custom_models",
            custom_models
        )

        self.models_changed.emit()


    def remove_custom_model(
        self,
        name: str,
    ) -> None:

        # Ищем модель
        model = next(
            (model for model in self.models
                if model.name == name
                and not model.builtin
            ),
            None
        )

        if model is None:
            raise ValueError(
                f"Пользовательская модель '{name}' не найдена"
            )

        self.models.remove(model)

        custom_models = self.settings.get(
            "ai.custom_models"
        ) or []

        custom_models = [
            item
            for item in custom_models
            if item["name"] != name
        ]

        self.settings.set(
            "ai.custom_models",
            custom_models
        )

        self.models_changed.emit()

    



