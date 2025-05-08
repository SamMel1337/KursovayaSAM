import json
import logging
from datetime import datetime
from typing import Union

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def analyze_cashback(year: int, month: int, excel_file: str) -> Union[str, None]:
    """
    Функция анализирует кэшбэк за указанный год и месяц,
    читая данные из Excel файла.
    """
    # Логирование начала выполнения функции
    logging.info(f"Запуск функции с годом: {year}, месяц: {month}")

    # Чтение данных из Excel файла
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        logging.error(f"Ошибка при чтении файла Excel: {e}")
        return json.dumps({"error": "Ошибка при чтении файла Excel"}, ensure_ascii=False)

    # Здесь можно добавить логику анализа данных
    # Например, фильтрация по году и месяцу и расчет кэшбэка

    # Пример возврата успешного результата (замените на вашу логику)
    result = {"message": "Анализ завершен успешно"}

    return json.dumps(result, ensure_ascii=False)

    # Проверка наличия необходимых колонок
    required_columns = ["Дата платежа", "Категория", "Кэшбэк"]
    if not all(column in df.columns for column in required_columns):
        logging.error("Отсутствуют необходимые колонки в Excel файле.")
        return json.dumps({"error": "Отсутствуют необходимые колонки в Excel файле."}, ensure_ascii=False)

    try:
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y", dayfirst=True)
    except Exception as e:
        logging.error(f"Ошибка при преобразовании дат: {e}")
        return json.dumps({"error": "Ошибка при преобразовании дат."}, ensure_ascii=False)

    # Преобразуем год и месяц в формат даты
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

    # Фильтрация транзакций по дате
    filtered_transactions = df[
        (pd.to_datetime(df["Дата платежа"]) >= start_date) & (pd.to_datetime(df["Дата платежа"]) < end_date)
    ]

    # Подсчет кешбэка по категориям
    cashback_by_category = filtered_transactions.groupby("Категория")["Кэшбэк"].sum().to_dict()

    # Формирование ответа
    response = {"year": year, "month": month, "cashback_by_category": cashback_by_category}

    # Логирование успешного завершения функции
    logging.info("Функция выполнена успешно, формирование ответа")

    # Возврат JSON-ответа
    return json.dumps(response, ensure_ascii=False)


# Пример использования функции
if __name__ == "__main__":
    excel_file = "../data/operations.xlsx"  # Укажите путь к вашему файлу Excel
    result = analyze_cashback(2019, 1, excel_file)
    print(result)
