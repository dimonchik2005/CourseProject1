from pathlib import Path

import pandas as pd

from src.reports import report_to_file, spending_by_category


def test_spending_by_category() -> None:
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-10-01",
                "Категория": "Супермаркеты",
                "Сумма платежа": -1000,
            },
            {
                "Дата операции": "2021-11-15",
                "Категория": "Супермаркеты",
                "Сумма платежа": -500,
            },
            {
                "Дата операции": "2021-12-01",
                "Категория": "Аптеки",
                "Сумма платежа": -300,
            },
            {
                "Дата операции": "2021-07-01",
                "Категория": "Супермаркеты",
                "Сумма платежа": -999,
            },
        ]
    )

    result = spending_by_category(transactions, "Супермаркеты", "2021-12-31")

    assert len(result) == 2
    assert result.iloc[0]["Сумма платежа"] == -1000
    assert result.iloc[1]["Сумма платежа"] == -500


def test_spending_by_category_empty_dataframe() -> None:
    transactions = pd.DataFrame()

    result = spending_by_category(transactions, "Супермаркеты", "2021-12-31")

    assert result.empty


def test_spending_by_category_no_matching_category() -> None:
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-12-01",
                "Категория": "Аптеки",
                "Сумма платежа": -300,
            }
        ]
    )

    result = spending_by_category(transactions, "Супермаркеты", "2021-12-31")

    assert result.empty


def test_report_to_file(tmp_path: Path) -> None:
    report_path = tmp_path / "test_report.json"

    @report_to_file(str(report_path))
    def test_report() -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "Категория": "Супермаркеты",
                    "Сумма платежа": -1000,
                }
            ]
        )

    result = test_report()

    assert not result.empty
    assert report_path.exists()
    assert "Супермаркеты" in report_path.read_text(encoding="utf-8")
