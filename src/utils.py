import json
from typing import Any

import pandas as pd


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Считывает Excel-файл с транзакциями и возвращает DataFrame."""
    print("Пробую открыть файл:", file_path)

    try:
        dataframe = pd.read_excel(file_path)
    except FileNotFoundError:
        print("Файл не найден:", file_path)
        return pd.DataFrame()

    print("Файл прочитан. Размер таблицы:", dataframe.shape)
    return dataframe


def read_user_settings(file_path: str) -> dict[str, Any]:
    """Считывает пользовательские настройки из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"user_currencies": [], "user_stocks": []}

    if not isinstance(data, dict):
        return {"user_currencies": [], "user_stocks": []}

    return data