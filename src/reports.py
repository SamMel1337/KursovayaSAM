import json
import logging
from datetime import datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_expenses_by_category(transactions_df: str, category: str, reference_date: str) -> str:
    """
    Функция для получения расходов по категории за трехмесячный период.
    """

    # Чтение данных из Excel файла
    df = pd.read_excel(transactions_df, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    try:
        # Преобразуем строку даты в объект datetime
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
        three_months_ago = reference_date - timedelta(days=90)

        # Фильтруем DataFrame по категории и дате
        filtered_df = df[
            (df["Категория"] == category)
            & (df["Дата операции"] >= three_months_ago)
            & (df["Дата операции"] <= reference_date)
            ]

        # Суммируем траты
        total_expenses = filtered_df["Сумма операции"].sum()

        # Формируем результат в виде словаря и преобразуем даты в строковый формат
        result = {
            "category": category,
            "total_expenses": total_expenses,
            "transactions": [
                {
                    **transaction,
                    "Дата операции": transaction["Дата операции"].strftime("%Y-%m-%d"),  # Преобразуем дату в строку
                }
                for transaction in filtered_df.to_dict(orient="records")
            ],
        }

        logger.info(f"Expenses calculated for category: {category}")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Ошибка при обработке данных: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Error while calculating expenses: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # Получение отчета
    json_report = get_expenses_by_category("../data/operations.xlsx", "Переводы", "2019-04-20")
    print(json_report)

# transactions_df = "../data/operations.xlsx"
# result = get_expenses_by_category(transactions_df, "Пополнения", "2019-01-01")  # Передаем дату в строковом формате
# print(result)
