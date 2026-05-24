from pathlib import Path

from src.reports import spending_by_category
from src.utils import read_excel_file

ROOT_DIR = Path(__file__).resolve().parent.parent
transactions = read_excel_file(str(ROOT_DIR / "data" / "operations.xlsx"))

report = spending_by_category(transactions, "Супермаркеты", "2021-12-31")

print(report.head())
print("Количество строк:", len(report))
