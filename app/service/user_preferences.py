import os
from typing import List

data_dir = os.path.abspath("./data")


def get_user_preferences_from_db() -> List[str]:
    file_path = os.path.join(data_dir, "user_preferences.txt")
    with open(file_path, "r") as f:
        user_preferences = [line.strip() for line in f.readlines()]
    return user_preferences
