import json
from datetime import datetime
from typing import Any

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, read_user_settings


def get_greeting(date_time: str) -> str:
    """Возвращает приветствие в зависимости от времени."""
    hour = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").hour

    if 6 <= hour <= 11:
        return "Доброе утро"
    if 12 <= hour <= 17:
        return "Добрый день"
    if 18 <= hour <= 22:
        return "Добрый вечер"

    return "Доброй ночи"


def filter_transactions_by_month(
    transactions: pd.DataFrame,
    date_time: str,
) -> pd.DataFrame:
    """Возвращает транзакции с начала месяца до указанной даты."""
    current_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_date = current_date.replace(day=1)

    transactions = transactions.copy()
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        errors="coerce",
    )

    return transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= current_date)
    ]


def get_cards_info(transactions: pd.DataFrame) -> list[dict[str, Any]]:
    """Возвращает информацию по картам: последние цифры, траты и кешбэк."""
    if transactions.empty or "Номер карты" not in transactions.columns:
        return []

    expenses = transactions[transactions["Сумма платежа"] < 0].copy()
    expenses["Сумма платежа"] = expenses["Сумма платежа"].abs()

    grouped = expenses.groupby("Номер карты")["Сумма платежа"].sum()

    return [
        {
            "last_digits": str(card),
            "total_spent": round(float(total), 2),
            "cashback": round(float(total) / 100, 2),
        }
        for card, total in grouped.items()
    ]


def get_top_transactions(transactions: pd.DataFrame) -> list[dict[str, Any]]:
    """Возвращает топ-5 транзакций по сумме платежа."""
    if transactions.empty:
        return []

    top_transactions = transactions.copy()
    top_transactions["abs_amount"] = top_transactions["Сумма платежа"].abs()
    top_transactions = top_transactions.sort_values(
        by="abs_amount",
        ascending=False,
    ).head(5)

    result = []

    for _, row in top_transactions.iterrows():
        date = pd.to_datetime(row["Дата операции"]).strftime("%d.%m.%Y")
        result.append(
            {
                "date": date,
                "amount": round(float(row["Сумма платежа"]), 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return result


def main_page(
    date_time: str,
    transactions: pd.DataFrame,
    settings_path: str = "user_settings.json",
) -> str:
    """Возвращает JSON-ответ для страницы Главная."""
    filtered_transactions = filter_transactions_by_month(transactions, date_time)
    settings = read_user_settings(settings_path)

    response = {
        "greeting": get_greeting(date_time),
        "cards": get_cards_info(filtered_transactions),
        "top_transactions": get_top_transactions(filtered_transactions),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
