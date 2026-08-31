from .client import PROVIDER_REGISTRY
from ai.config.models import ModelConfig


class ProviderManager:

    def __init__(self):
        self._provider = None

    @property
    def provider(self):
        return self._provider
    

    def select(self, model_info: ModelConfig):

        provider_name = model_info.provider
        
        provider_cls = PROVIDER_REGISTRY[provider_name]
            
        self._provider = provider_cls(model=model_info.model_id, name=provider_name)


    def ping(self):
        return self._provider.ping()