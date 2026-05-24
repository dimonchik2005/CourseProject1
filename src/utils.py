import json
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Считывает Excel-файл с транзакциями и возвращает DataFrame."""
    print("Пробую открыть файл:", file_path)

    try:
        dataframe = pd.read_excel(file_path)
    except FileNotFoundError:
        print("Файл не найден:", file_path)
        return pd.DataFrame()

    return dataframe


def read_user_settings(file_path: str) -> dict[str, Any]:
    """Считывает пользовательские настройки из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError, json.JSONDecodeError:
        return {"user_currencies": [], "user_stocks": []}

    if not isinstance(data, dict):
        return {"user_currencies": [], "user_stocks": []}

    return data


load_dotenv()


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """Возвращает курсы валют к рублю."""
    api_key = os.getenv("CURRENCY_API_KEY")
    result = []

    for currency in currencies:
        try:
            response = requests.get(
                "https://api.apilayer.com/exchangerates_data/latest",
                headers={"apikey": api_key},
                params={"base": currency, "symbols": "RUB"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            rate = float(data["rates"]["RUB"])
        except Exception:
            rate = 0.0

        result.append({"currency": currency, "rate": rate})

    return result


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Возвращает цены акций."""
    result = []

    for stock in stocks:
        result.append({"stock": stock, "price": 100.0})

    return result
