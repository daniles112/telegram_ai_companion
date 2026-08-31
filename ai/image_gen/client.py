from os import getenv
from dotenv import load_dotenv
from ut.bot_utils import image_url_to_bytes
from .default_negatives import DEFAULT_NEGATIVES
from dataclasses import dataclass
from io import BytesIO
import httpx




load_dotenv()


class ImageGenerationError(Exception):
    pass


class IncorrectParams(Exception):
    pass


@dataclass
class GenerationResult:
    image: BytesIO
    image_url: str
    preview_url: str

    provider: str

    prompt: str
    negative_prompt: str

    model_type: str
    model: str

    width: int
    height: int

    steps: int
    cfg_scale: float

    cost: int

    raw_response: dict



class CivitaiClient:

    def __init__(self):
        self._api = getenv("CIVITAI_API_KEY")
        self.provider = "civitai"
        self.client = httpx.AsyncClient(
            base_url="https://orchestration.civitai.com",
            headers={
                "Authorization": f"Bearer {self._api}",
                "Content-Type": "application/json"
            },
            timeout=90,
            follow_redirects=True
        )
        self.model_presets={
            "sdxl": {
                "engine": "sdcpp",
                "ecosystem": "sdxl",
                "operation": "createImage",
                "model": "urn:air:sdxl:checkpoint:civitai:1717562@3152323",
                "prompt": "",
                "negativePrompt": DEFAULT_NEGATIVES["sdxl"], 
                "width": 1024,
                "height": 1024,
                "cfgScale": 7,
                "steps": 25
            },
            "anima": {
                "engine": "sdcpp",
                "ecosystem": "anima",
                "operation": "createImage",
                "prompt": "",
                "negativePrompt": DEFAULT_NEGATIVES["anima"],
                "width": 1024,
                "height": 1024,
                "cfgScale": 4,
                "steps": 30,
                "diffuserModel": "urn:air:anima:checkpoint:civitai:2458426@3126581"
            }
        }


    async def close(self):
        await self.client.aclose()


    async def generate_image(self,
                    prompt: str, 
                    negative_prompt: str | None = None,
                    model_type: str = "sdxl", 
                    model: str | None = None,
                    width: int = 1024,
                    height: int = 1024,
                    cfg_scale: int = -1,
                    steps: int = -1
                    ) -> GenerationResult:


        try:
            workflow = self.model_presets[model_type].copy()
            workflow["prompt"] = prompt

            if negative_prompt:
                workflow["negativePrompt"] = negative_prompt

            if model:
                if "model" in workflow:
                    workflow["model"] = model
                else:
                    workflow["diffuserModel"] = model

            workflow["width"] = width
            workflow["height"] = height

            if 15 >= cfg_scale > 0:
                workflow["cfgScale"] = cfg_scale

            if 50 >= steps > 0:
                workflow["steps"] = steps


        except Exception as e:
            raise IncorrectParams(e)


        json = {
            "steps": [
                {
                    "$type": "imageGen",
                    "input": workflow
                }
            ],
        }


        response = await self.client.post(
            "/v2/consumer/workflows",
            params={
                "wait": 60
            },
            json=json
        )
        response.raise_for_status()
        result = response.json()
        step = result["steps"][0]
        if step["status"] != "succeeded":
            errors = step["output"].get("errors", [])
            raise ImageGenerationError(errors)

        image = step["output"]["images"][0]
        image_url = image["url"]
        
        generation_result = GenerationResult(
            image=await image_url_to_bytes(image_url, self.client),
            image_url=image_url,
            preview_url=image["previewUrl"],
            provider=self.provider,
            prompt=prompt,
            negative_prompt=workflow["negativePrompt"],
            model_type=model_type,
            model=workflow.get("model") or workflow.get("diffuserModel"),
            width=width,
            height=height,
            steps=workflow["steps"],
            cfg_scale=workflow["cfgScale"],
            cost=result["cost"]["total"],
            raw_response=result
        )

        return generation_result

