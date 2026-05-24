import json
from unittest.mock import patch

import pandas as pd

from src.views import (filter_transactions_by_month, get_cards_info,
                       get_greeting, get_top_transactions, main_page)


def test_get_greeting_morning() -> None:
    assert get_greeting("2021-12-21 07:00:00") == "Доброе утро"


def test_get_greeting_day() -> None:
    assert get_greeting("2021-12-21 13:00:00") == "Добрый день"


def test_get_greeting_evening() -> None:
    assert get_greeting("2021-12-21 19:00:00") == "Добрый вечер"


def test_get_greeting_night() -> None:
    assert get_greeting("2021-12-21 23:30:00") == "Доброй ночи"


def test_filter_transactions_by_month() -> None:
    transactions = pd.DataFrame(
        [
            {"Дата операции": "2021-12-01 10:00:00", "Сумма платежа": -100},
            {"Дата операции": "2021-12-15 10:00:00", "Сумма платежа": -200},
            {"Дата операции": "2021-11-30 10:00:00", "Сумма платежа": -300},
            {"Дата операции": "2021-12-25 10:00:00", "Сумма платежа": -400},
        ]
    )

    result = filter_transactions_by_month(transactions, "2021-12-20 23:59:59")

    assert len(result) == 2


def test_filter_transactions_by_month_empty_dataframe() -> None:
    transactions = pd.DataFrame()

    result = filter_transactions_by_month(transactions, "2021-12-20 23:59:59")

    assert result.empty


def test_get_cards_info() -> None:
    transactions = pd.DataFrame(
        [
            {
                "Номер карты": "5814",
                "Сумма платежа": -1000,
            },
            {
                "Номер карты": "5814",
                "Сумма платежа": -500,
            },
            {
                "Номер карты": "7512",
                "Сумма платежа": -200,
            },
            {
                "Номер карты": "7512",
                "Сумма платежа": 100,
            },
        ]
    )

    result = get_cards_info(transactions)

    assert result == [
        {
            "last_digits": "5814",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
        {
            "last_digits": "7512",
            "total_spent": 200.0,
            "cashback": 2.0,
        },
    ]


def test_get_cards_info_empty_dataframe() -> None:
    transactions = pd.DataFrame()

    assert get_cards_info(transactions) == []


def test_get_top_transactions() -> None:
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-12-01 10:00:00",
                "Сумма платежа": -100,
                "Категория": "Супермаркеты",
                "Описание": "Лента",
            },
            {
                "Дата операции": "2021-12-02 10:00:00",
                "Сумма платежа": -1000,
                "Категория": "Переводы",
                "Описание": "Перевод",
            },
            {
                "Дата операции": "2021-12-03 10:00:00",
                "Сумма платежа": -500,
                "Категория": "Аптеки",
                "Описание": "Аптека",
            },
        ]
    )

    result = get_top_transactions(transactions)

    assert len(result) == 3
    assert result[0]["amount"] == -1000.0
    assert result[0]["date"] == "02.12.2021"
    assert result[0]["category"] == "Переводы"
    assert result[0]["description"] == "Перевод"


def test_get_top_transactions_empty_dataframe() -> None:
    transactions = pd.DataFrame()

    assert get_top_transactions(transactions) == []


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.read_user_settings")
def test_main_page(
    mock_read_user_settings,
    mock_get_currency_rates,
    mock_get_stock_prices,
) -> None:
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-12-01 10:00:00",
                "Номер карты": "5814",
                "Сумма платежа": -1000,
                "Категория": "Супермаркеты",
                "Описание": "Лента",
            }
        ]
    )

    mock_read_user_settings.return_value = {
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL"],
    }
    mock_get_currency_rates.return_value = [
        {
            "currency": "USD",
            "rate": 90.5,
        }
    ]
    mock_get_stock_prices.return_value = [
        {
            "stock": "AAPL",
            "price": 150.0,
        }
    ]

    result = main_page("2021-12-21 12:00:00", transactions)
    result_data = json.loads(result)

    assert result_data["greeting"] == "Добрый день"
    assert result_data["cards"] == [
        {
            "last_digits": "5814",
            "total_spent": 1000.0,
            "cashback": 10.0,
        }
    ]
    assert result_data["currency_rates"] == [
        {
            "currency": "USD",
            "rate": 90.5,
        }
    ]
    assert result_data["stock_prices"] == [
        {
            "stock": "AAPL",
            "price": 150.0,
        }
    ]
