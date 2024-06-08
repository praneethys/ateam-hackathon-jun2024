import os
from typing import List

data_dir = os.path.abspath("./data")


def get_ingredients_from_db() -> List[str]:
    file_path = os.path.join(data_dir, "ingredients.txt")
    with open(file_path, "r") as f:
        ingredients = [line.strip() for line in f.readlines()]
    return ingredients
