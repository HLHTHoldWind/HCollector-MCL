"""Read language file"""

import json


def get_language(path) -> dict:
    with open(path) as file:
        content = json.load(file)
    return content
