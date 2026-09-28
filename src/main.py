from pathlib import Path

from src.reports import spending_by_category
from src.services import (search_person_transfers, search_phone_numbers,
                          simple_search)
from src.utils import read_excel_file
from src.views import main_page

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "operations.xlsx"


def main() -> None:
    """Запускает основные функции проекта."""
    transactions = read_excel_file(str(DATA_PATH))

    print("Главная страница:")
    print(main_page("2021-12-21 12:00:00", transactions))

    print("\nПростой поиск:")
    print(simple_search(transactions, "перевод")[:500])

    print("\nПоиск телефонных номеров:")
    print(search_phone_numbers(transactions)[:500])

    print("\nПоиск переводов физлицам:")
    print(search_person_transfers(transactions)[:500])

    print("\nОтчет по категории:")
    report = spending_by_category(transactions, "Супермаркеты", "2021-12-31")
    print(report.head())


if __name__ == "__main__":
    main()
