import json

def load_cards():
    with open("data/cards.json", "r", encoding="utf-8") as f:
        return json.load(f)
