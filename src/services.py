import json
import re
from typing import Any

import pandas as pd


def simple_search(transactions: pd.DataFrame, search_query: str) -> str:
    """Возвращает JSON со всеми транзакциями, содержащими запрос в описании или категории."""
    if transactions.empty:
        return json.dumps([], ensure_ascii=False)

    pattern = re.compile(search_query, re.IGNORECASE)

    filtered_transactions = transactions[
        transactions["Описание"].fillna(" ").astype(str).apply(lambda value: bool(pattern.search(value)))
        | transactions["Категория"]
        .fillna(" ").astype(str).apply(lambda value: bool(pattern.search(value)))
    ]

    return filtered_transactions.to_json(orient="records", force_ascii=False)


def search_phone_numbers(transactions: pd.DataFrame) -> str:
    """Возвращает JSON с транзакциями, содержащими телефонные номера в описании."""
    if transactions.empty:
        return json.dumps([], ensure_ascii=False)

    phone_pattern = re.compile(r"(\+7\s?\d{3}\s?\d{2,3}[-\s]?\d{2}[-\s]?\d{2}|8\d{10})")

    filtered_transactions = transactions[
        transactions["Описание"].fillna(" ").astype(str)
        .apply(lambda value: bool(phone_pattern.search(value)))
    ]

    return filtered_transactions.to_json(orient="records", force_ascii=False)


def search_person_transfers(transactions: pd.DataFrame) -> str:
    """Возвращает JSON с переводами физическим лицам."""
    if transactions.empty:
        return json.dumps([], ensure_ascii=False)

    person_name_pattern = re.compile(r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")

    filtered_transactions = transactions[
        (transactions["Категория"] == "Переводы")
        & transactions["Описание"].fillna(" ").astype(str)
        .apply(lambda value: bool(person_name_pattern.search(value)))
    ]

    return filtered_transactions.to_json(orient="records", force_ascii=False)
