# file_utils.py

import json


def load_from_json(filename: str) -> list[dict]:
    with open(filename, encoding='utf-8') as f:
        return json.load(f)


def save_to_json(data: list[dict], filename: str) -> None:
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
