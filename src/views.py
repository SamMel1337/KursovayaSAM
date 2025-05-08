import json
from typing import Optional

from src.reports import get_expenses_by_category
from src.services import analyze_cashback
from src.utils import (
    get_card_with_spend,
    get_ccurent,
    get_data_time,
    get_path_and_period,
    get_time_for_greeting,
    get_top_trans,
)


def main_info(date_time: str) -> str:
    """
    Получает информацию о пользователе на основе заданной даты и времени.
    """
    greenting = get_time_for_greeting()
    time_period = get_data_time(date_time)
    sorted_df = get_path_and_period("../data/operations.xlsx", time_period)
    cards = get_card_with_spend(sorted_df)
    top_trans = get_top_trans(sorted_df, 3)
    ccurent = get_ccurent("../data/user_settings.json")

    data = {"greeting": greenting, "cards": cards, "top_trans": top_trans, "ccurent": ccurent}
    json_date = json.dumps(data, ensure_ascii=False, indent=4)
    return json_date


def mai_per(year, month, excel_file) -> str:
    """
    Анализирует кэшбэк на основе переданных параметров.
    """

    ser = analyze_cashback(year, month, excel_file)

    data1 = {
        "ser": ser,
    }
    json_date1 = json.dumps(data1, ensure_ascii=False, indent=4)
    return json_date1


def new_main(transactions_df, category: str, date: Optional[str] = None):
    """
    Получает расходы по заданной категории и опционально по дате
    """
    reter = get_expenses_by_category(transactions_df, category, date)
    return reter
