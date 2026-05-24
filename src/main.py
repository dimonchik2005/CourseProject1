from src.utils import read_excel_file
from src.views import main_page

transactions = read_excel_file("data/operations.xlsx")

print(main_page("2021-12-21 12:00:00", transactions))
