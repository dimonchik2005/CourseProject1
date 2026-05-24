# CourseProject

Курсовой проект для анализа банковских транзакций из Excel-файла.

## Возможности

- чтение транзакций из Excel-файла;
- чтение пользовательских настроек из `user_settings.json`;
- генерация JSON-ответа для страницы "Главная";
- получение курсов валют через API;
- получение цен акций;
- простой поиск по описанию и категории;
- поиск транзакций с телефонными номерами;
- поиск переводов физическим лицам;
- формирование отчета "Траты по категории";
- запись отчета в JSON-файл через декоратор;
- логирование работы приложения.

## Структура проекта

```
src/
├── main.py
├── utils.py
├── views.py
├── services.py
├── reports.py
└── logger_config.py

tests/
├── test_utils.py
├── test_views.py
├── test_services.py
├── test_reports.py
└── conftest.py

data/
└── operations.xlsx
```
## Установка
`poetry install`
## Запуск
`poetry run python -m src.main`
## Используемые линтеры

- poetry run black .
- poetry run isort .
- poetry run flake8
- poetry run mypy src tests