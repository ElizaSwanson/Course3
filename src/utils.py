import datetime
import datetime as dt
import json
import logging
import os

import pandas as pd
import pytest
import requests
from dotenv import load_dotenv

load_dotenv("..\\.env")

path_to_log = "logs/utils.log"
abs_path = os.path.abspath(path_to_log)


logger_utils = logging.getLogger("utils")
utils_handler = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
utils_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
utils_handler.setFormatter(utils_formatter)
logger_utils.addHandler(utils_handler)
logger_utils.setLevel(logging.DEBUG)


def reading_excel(path_to_file: str) -> list[dict]:
    logger_utils.info(f"Пытаюсь прочитать файл {path_to_file}")
    try:
        df_list = pd.read_excel(path_to_file)
        logger_utils.info("Считано!")
        return df_list
    except FileNotFoundError:
        logger_utils.error("Нельзя прочитать то, чего нет!")
        raise


def get_dict_transaction(file_path) -> list[dict]:
    """Функция преобразовывающая датафрейм в словарь pyhton"""

    logger_utils.info(f"Начинаем преобразовывать {file_path}...")
    try:
        df = pd.read_excel(file_path)
        logger_utils.info(f"Файл {file_path}  прочитан")
        dict_transaction = df.to_dict(orient="records")
        logger_utils.info("Список словарей создан")
        return dict_transaction
    except FileNotFoundError:
        logger_utils.error("Нельзя прочитать то, чего нет")
        raise
    except Exception as e:
        logger_utils.error(f"Произошла ошибка: {str(e)}")
        raise


def get_data(data: str) -> datetime.datetime:
    logger_utils.info(f"Получена дата: {data}")
    try:
        data_now = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger_utils.info("Дата преобразована")
        return data_now
    except Exception as e:
        logger_utils.info(f"Ошибка: {e}")
        return e


def get_greeting():
    """Функция приветствия пользователя в зависимости от времени суток"""
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_expenses_cards(transactions_list_excel) -> list[dict]:
    """Информация о расходах по каждой карте"""
    logger_utils.info("Начинаем выполнять функцию...")

    all_cards_info = (
        transactions_list_excel.loc[transactions_list_excel["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    logger_utils.debug(f"Получены расходы по всем картам: {all_cards_info}")

    spent_cards = []
    for card, spent in all_cards_info.items():
        spent_cards.append(
            {
                "last_digits": card,
                "total spent": abs(spent),
                "cashback": abs(round(spent / 100)),
            }
        )
        logger_utils.info(f"Добавлен расход по карте {card}: {spent}")

    logger_utils.info("Завершение выполнения функции get_expenses_cards")
    return spent_cards


def top_transaction(trans_list_excel):
    """Выводит топ-5 самых дорогих платежей по карте"""
    logger_utils.info("Начинаем вычислять топ-5 транзакций")
    top_transaction = trans_list_excel.sort_values(
        by="Сумма платежа", ascending=True
    ).iloc[:5]
    logger_utils.info("Сформирован список из 5 транзакций")
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                "date": str(
                    (
                        datetime.datetime.strptime(
                            transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"
                        )
                    )
                    .date()
                    .strftime("%d.%m.%Y")
                ).replace("-", "."),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    if top_transaction_list:
        logger_utils.info("Список готов")
        return top_transaction_list
    else:
        logger_utils.error("Список не найден")
        return None


def get_stock_price(stocks: list) -> list:
    """Функция для вывода стоимости акций"""
    logger_utils.info("Ищем курсы акций...")
    api_key = os.getenv("API_KEY_Stocks")
    stock_price = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        data_ = response.json()
        stock_price.append(
            {
                "stock": stock,
                "price": round(float(data_["Global Quote"]["05. price"]), 2)
            }
        )
    logger_utils.info("Функция завершила свою работу")
    return stock_price


def get_currency_rates(currencies):
    """функция для вывода текущего курса евро и доллара"""

    logger_utils.info("Получаем стоимость валют...")
    api_key = os.environ.get("API_KEY_Currency")
    url = f"https://api.apilayer.com/currency_data/live?base=RUB&symbols={currencies}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    quotes = data.get("quotes")
    usd = quotes.get("USDRUB")
    eur_usd = quotes.get("USDEUR")
    eur = usd / eur_usd
    logger_utils.info("Успешно!")
    rates = [
            {"currency": "USD", "rate": round(usd, 2)},
            {"currency": "EUR", "rate": round(eur, 2)},
        ]
    return rates


def get_user_setting(path_to_file: str):
    """Функция перевода настроек пользователя(курс и акции) из json объекта"""
    logger_utils.info("Вызываем пользовательские настройки")
    with open(path_to_file, "r", encoding="utf-8") as f:
        user_setting = json.load(f)
        logger_utils.info("Получены настройки пользователя")
    return user_setting["user_currencies"], user_setting["user_stocks"]


def transaction_currency(
    transactions_list_excel: pd.DataFrame, data: str
) -> pd.DataFrame:
    """функция формирует расходы в нужном интервале"""
    fin_data = get_data(data)
    logger_utils.debug(f"Конечная дата: {fin_data}")
    start_data = fin_data.replace(day=1)
    logger_utils.debug(f"Начальная дата: {start_data}")
    fin_data = fin_data.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + dt.timedelta(days=1)
    logger_utils.debug(f"Обновлена конечная дата: {fin_data}")
    transaction_currency = transactions_list_excel.loc[
        (
            pd.to_datetime(transactions_list_excel["Дата операции"], dayfirst=True)
            <= fin_data
        )
        & (
            pd.to_datetime(transactions_list_excel["Дата операции"], dayfirst=True)
            >= start_data
        )
    ]
    return transaction_currency
