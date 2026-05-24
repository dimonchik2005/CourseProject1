from datetime import datetime
from functools import wraps
from typing import Any, Callable

import pandas as pd


def report_to_file(filename: str = "report.json") -> Callable:
    """Записывает результат работы функции-отчета в файл."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
            result = func(*args, **kwargs)
            result.to_json(
                filename,
                orient="records",
                force_ascii=False,
                indent=4,
                date_format="iso",
            )
            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: str | None = None,
) -> pd.DataFrame:
    """Возвращает траты по категории за последние три месяца."""
    if transactions.empty:
        return pd.DataFrame()

    current_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()

    start_date = current_date - pd.DateOffset(months=3)

    transactions = transactions.copy()
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        errors="coerce",
    )

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= current_date)
        & (transactions["Категория"] == category)
        & (transactions["Сумма платежа"] < 0)
    ]

    return filtered_transactions
