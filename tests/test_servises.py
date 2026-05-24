import json

import pandas as pd

from src.services import (search_person_transfers, search_phone_numbers,
                          simple_search)


def test_simple_search_by_description(sample_transactions: pd.DataFrame) -> None:
    result = simple_search(sample_transactions, "валерий")
    result_data = json.loads(result)

    assert len(result_data) == 1
    assert result_data[0]["Описание"] == "Валерий А."


def test_simple_search_by_category() -> None:
    data = pd.DataFrame(
        [
            {"Описание": "Лента", "Категория": "Супермаркеты"},
            {"Описание": "Такси", "Категория": "Транспорт"},
        ]
    )

    result = simple_search(data, "супермаркеты")
    result_data = json.loads(result)

    assert len(result_data) == 1
    assert result_data[0]["Категория"] == "Супермаркеты"


def test_simple_search_empty_dataframe() -> None:
    data = pd.DataFrame()

    result = simple_search(data, "перевод")

    assert json.loads(result) == []


def test_simple_search_not_found() -> None:
    data = pd.DataFrame(
        [
            {"Описание": "Лента", "Категория": "Супермаркеты"},
        ]
    )

    result = simple_search(data, "аптека")

    assert json.loads(result) == []


def test_search_phone_numbers() -> None:
    data = pd.DataFrame(
        [
            {"Описание": "МТС +7 921 111-22-33", "Категория": "Связь"},
            {"Описание": "Лента", "Категория": "Супермаркеты"},
            {"Описание": "Пополнение 89000000000", "Категория": "Связь"},
        ]
    )

    result = search_phone_numbers(data)
    result_data = json.loads(result)

    assert len(result_data) == 2
    assert result_data[0]["Описание"] == "МТС +7 921 111-22-33"
    assert result_data[1]["Описание"] == "Пополнение 89000000000"


def test_search_phone_numbers_empty_dataframe() -> None:
    data = pd.DataFrame()

    result = search_phone_numbers(data)

    assert json.loads(result) == []


def test_search_person_transfers() -> None:
    data = pd.DataFrame(
        [
            {"Описание": "Валерий А.", "Категория": "Переводы"},
            {"Описание": "Сергей З.", "Категория": "Переводы"},
            {"Описание": "Лента", "Категория": "Супермаркеты"},
            {"Описание": "Перевод организации", "Категория": "Переводы"},
        ]
    )

    result = search_person_transfers(data)
    result_data = json.loads(result)

    assert len(result_data) == 2
    assert result_data[0]["Описание"] == "Валерий А."
    assert result_data[1]["Описание"] == "Сергей З."


def test_search_person_transfers_empty_dataframe() -> None:
    data = pd.DataFrame()

    result = search_person_transfers(data)

    assert json.loads(result) == []
