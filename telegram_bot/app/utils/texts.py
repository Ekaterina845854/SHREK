import json

def load_texts(lang="ru"):
    with open(f"./app/texts/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)

texts = load_texts()