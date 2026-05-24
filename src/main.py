from src.utils import read_excel_file, read_user_settings


transactions = read_excel_file("data/operations.xlsx")
settings = read_user_settings("user_settings.json")

print(transactions.head())
print(settings)