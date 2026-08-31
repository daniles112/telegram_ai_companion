from pathlib import Path
import json


BASE_DIR = Path(__file__).parent.parent


def select_model() -> dict:
    with open(BASE_DIR / "ai" / "config" / "providers.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    model_list = list(enumerate(config.keys()))

    for i, name in model_list:
        print(f"{i}. {name}")

    while True:

        inp = input("Выберете модель: >> ")

        try:
            inp = int(inp)
            index = max(min(inp, len(model_list)), 1)
            name = model_list[index-1][1]

            print("Выбрана модель:", name)

            return config[name]
        
        except Exception as e:
            print("Неверный ввод")
            print(e)