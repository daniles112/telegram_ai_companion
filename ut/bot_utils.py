from io import BytesIO
from random import randint
from httpx import AsyncClient
import asyncio
import re
from pathlib import Path
import json



BASE_DIR = Path(__file__).parent.parent




def parse_image_params(text: str):

    params = {}

    # тип модели
    model = re.search(r"==mtype\s+(\w+)", text)
    if model:
        params["model_type"] = model.group(1)

    # модель
    model = re.search(r"==model\s+(\w+)", text)
    if model:
        params["model"] = model.group(1)

    # размер
    size = re.search(r"==size\s+(\d+)x(\d+)", text)
    if size:
        params["width"] = int(size.group(1))
        params["height"] = int(size.group(2))

    # steps
    steps = re.search(r"==steps\s+(\d+)", text)
    if steps:
        params["steps"] = int(steps.group(1))

    # cfg
    cfg = re.search(r"==cfg\s+(\d+)", text)
    if cfg:
        params["cfg_scale"] = int(cfg.group(1))


    # удаляем параметры из текста
    prompt = re.sub(r"==\w+\s+(?:\"[^\"]*\"|\S+)",
    "",
    text)

    # чистим пробелы
    prompt = prompt.strip()

    return prompt, params



def get_chat_title(message):

    if message.chat.type == "private":
        return message.from_user.first_name

    return message.chat.title




async def image_url_to_bytes(url: str, client: AsyncClient) -> BytesIO:

    response = await client.get(url)
    response.raise_for_status()

    image = BytesIO(response.content)
    image.name = f"image_{randint(10000, 99999)}.jpg"

    return image