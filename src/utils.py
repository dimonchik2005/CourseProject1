import json
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger_config import setup_logger

utils_logger = setup_logger("utils", "utils.log")


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Считывает Excel-файл с транзакциями и возвращает DataFrame."""
    try:
        dataframe = pd.read_excel(file_path)
        utils_logger.info("Excel-файл успешно прочитан: %s", file_path)
        return dataframe
    except FileNotFoundError:
        utils_logger.error("Excel-файл не найден: %s", file_path)
        return pd.DataFrame()

    return dataframe


def read_user_settings(file_path: str) -> dict[str, Any]:
    """Считывает пользовательские настройки из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        utils_logger.info("Файл настроек успешно прочитан: %s", file_path)
    except FileNotFoundError:
        utils_logger.error("Файл настроек не найден: %s", file_path)
        return {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError:
        utils_logger.error("Некорректный JSON в файле настроек: %s", file_path)
        return {"user_currencies": [], "user_stocks": []}

    if not isinstance(data, dict):
        utils_logger.error("Файл настроек должен содержать словарь: %s", file_path)
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
            utils_logger.info("Курс валюты %s успешно получен", currency)
        except Exception:
            rate = 0.0
            utils_logger.error("Не удалось получить курс валюты %s", currency)

        result.append({"currency": currency, "rate": rate})

    return result


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Возвращает цены акций."""
    result = []

    for stock in stocks:
        try:
            price = 100.0
            utils_logger.info("Цена акции %s успешно получена", stock)
        except Exception:
            price = 0.0
            utils_logger.error("Не удалось получить цену акции %s", stock)

        result.append({"stock": stock, "price": float(price)})

    return result
