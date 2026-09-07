from .client import PROVIDER_REGISTRY
from ai.config.models import ModelConfig
from ai.config.settings_manager import SettingsManager


class ProviderManager:

    def __init__(self, settings: SettingsManager):
        self._provider = None
        self._settings = settings

    @property
    def provider(self):
        return self._provider
    

    def select(self, model_info: ModelConfig):

        provider_name = model_info.provider
        
        provider_cls = PROVIDER_REGISTRY[provider_name]
            
        self._provider = provider_cls(settings=self._settings,
                                      model=model_info.model_id, 
                                      name=provider_name)


    def ping(self):
        return self._provider.ping()