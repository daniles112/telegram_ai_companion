from os import getenv
from dotenv import load_dotenv
from openai import AsyncOpenAI
from abc import ABC




load_dotenv()


PROVIDER_REGISTRY = {}

def register(name):

    def wrapper(cls):
        PROVIDER_REGISTRY[name] = cls
        return cls
    
    return wrapper




class OpenAIProvider(ABC):
    def __init__(self,
                settings,
                name, 
                model, 
                timeout=20.0,
                max_retries=3,
                max_tokens=1500):
        
        self.name = name
        self.settings = settings
        self.api_key = settings.get(f"ai.providers.{self.name}.api_key")
        self.base_url = settings.get(f"ai.providers.{self.name}.base_url")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_tokens = max_tokens
        self.client = self.create_client()


    def create_client(self):

        return AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )

    
    async def ask_llm(self, history, system_prompt):
    
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    *history
                    ],
                )
            
            return {
                "text": response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "answer_tokens": response.usage.completion_tokens,
                "model": self.model,
                "provider": self.name
            }


    async def ping(self) -> bool:
        try:
            await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "ping"
                    }
                ],
                max_tokens=1
            )
    
            return {
                "result": True,
                "errors": None
            }
    
        except Exception as e:
            print(repr(e))
            return {
                    "result": False,
                    "errors": e
                }


    




@register("groq")
class GroqProvider(OpenAIProvider):

    def __init__(self,
                settings,
                model,
                name):
        
        super().__init__(settings=settings,
                         model=model,
                         name=name)



    async def ask_llm(self, history, system_prompt):

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *history
                ],
            )
        
        return {
                "text": response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "answer_tokens": response.usage.completion_tokens,
                "model": self.model,
                "provider": self.name
            }





@register("openai")
class OpenAIProvider(OpenAIProvider):

    def __init__(self,
                settings,
                model,
                name):
        
        super().__init__(settings=settings,
                         model=model,
                         name=name)


    async def ping(self) -> bool:
        try:
            await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "ping"
                    }
                ]
            )
    
            return {
                    "result": True,
                    "errors": None
                }
        
        except Exception as e:
            print(repr(e))
            return {
                    "result": False,
                    "errors": e
                }


        
        
@register("openrouter")
class OpenRouterProvider(OpenAIProvider):

    def __init__(self,
                settings,
                model,
                name):
        
        super().__init__(settings=settings,
                         model=model,
                         name=name)
        
        
        
