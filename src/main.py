from pathlib import Path

from src.services import (search_person_transfers, search_phone_numbers,
                          simple_search)
from src.utils import read_excel_file

ROOT_DIR = Path(__file__).resolve().parent.parent
transactions = read_excel_file(str(ROOT_DIR / "data" / "operations.xlsx"))

print(simple_search(transactions, "перевод"))
print(search_phone_numbers(transactions))
print(search_person_transfers(transactions))
