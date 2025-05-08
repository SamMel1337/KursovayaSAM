import json
import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
import requests
from pandas import DataFrame

logging.basicConfig(level=logging.INFO)
URL = "https://api.apilayer.com/currency_data/convert"
API = "m3gjTclxrCxcREmfnJflQZ7qadOTc5yY"


def get_time_for_greeting() -> str:
    """Функция возращает приветсивие, в зависимости от времени"""
    user_datetime = datetime.now().hour
    if 5 <= user_datetime < 12:
        return "Доброе утро"
    elif 12 <= user_datetime < 18:
        return "Добрый дeнь"
    elif 18 <= user_datetime < 22:
        return "Добрый вечер"
    else:
        return "Добрый день"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [start_of_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def get_path_and_period(path_to_file: str, period_date: list) -> DataFrame:
    """Функия принимает путь к exсel"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    # print("We here")
    # print(type(pd.to_datetime(df["Дата операции"], dayfirst = True)))
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    logging.info("Функция выполнена успешно, формирование ответа")
    # print(sorted_df)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> List[Dict[str, float]]:
    """
    Функция принимает DataFrame и возвращает список с расходами.
    """
    carts_spends = []
    card_sorted = sorted_df[["Номер карты", "Сумма операции", "Кэшбэк", "Сумма операции с округлением"]]

    for _, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"])[-4:]  # Получаем последние 4 цифры номера карты
            total_spent = abs(row["Сумма операции с округлением"])  # Берем абсолютное значение
            cashback = total_spent // 100

            spend_info = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback
            }
            carts_spends.append(spend_info)

    logging.info("Функция выполнена успешно, формирование ответа")
    return carts_spends

def get_top_trans(sorted_df: DataFrame, top: int) -> List[Dict[str, str]]:
    """
    Функция возвращает топ N транзакций по сумме платежа.
    """
    top_per_tran = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_tran = sorted_pay_df.head(top)
    top_tran_sor = top_tran[["Дата платежа", "Сумма операции", "Категория", "Описание"]]

    for _, j1 in top_tran_sor.iterrows():
        j1_dict = {
            "date": f"{j1['Дата платежа']}",
            "amount": f"{j1['Сумма операции']}",
            "category": f"{j1['Категория']}",
            "description": f"{j1['Описание']}",
        }
        top_per_tran.append(j1_dict)
    logging.info("Функция выполнена успешно, формирование ответа")

    return top_per_tran


def get_ccurent(part_json: str) -> List[Dict[str, str]]:
    """
    Получает текущие курсы валют на основе данных из JSON-файла.
    """
    curen = []
    with open(part_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        currebt = data["user_currencies"]

        for cru in currebt:
            params = {"amount": 1, "from": f"{cru}", "to": "RUB"}
            headers = {"apikey": f"{API}"}
            response = requests.request("GET", URL, headers=headers, data=params)

            starus_code = response.status_code
            if starus_code == 200:
                resuit = response.json()
                curren_rate = resuit["query"]["from"]
                cer_an = round(resuit["resuit"], 2)
                curen.append({"ccurrency": f"{curren_rate}", "rate": f"{cer_an}"})
            logging.info("Функция выполнена успешно, формирование ответа")
        return curen
