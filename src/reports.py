import datetime
import datetime as dt
import logging
from functools import wraps
from typing import Any, Callable
import pandas as pd
from src.utils import get_data, reading_excel

logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
reports_handler = logging.FileHandler("..\\logs\\reports.log", encoding="utf-8")
repots_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
reports_handler.setFormatter(repots_formatter)
logger.addHandler(reports_handler)


def decorator_log(filename: Any = None) -> Callable:
    """Декоратор логирует вызов функции и результат вызова"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write("\n my function is OK")
                else:
                    print("\n my function is OK")
            except Exception as e:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(
                            f"\n my function error: {e}, inputs: {args}, {kwargs} \n"
                        )
                else:
                    print(f"\n my function error: {e}, inputs: {args}, {kwargs} \n")
            return wrapper

        return wrapper

    return decorator


def spending_by_category(
    df_transactions: pd.DataFrame, category: str, date: [str] = None
) -> pd.DataFrame:
    """Функция возвращает траты по категории за последние три месяца. Если дата не указана, берется текущая"""
    if date is None:
        picked_data = dt.datetime.now()
    else:
        picked_data = get_data(date)
    earlier_data = picked_data.replace(hour=0, minute=0, second=0) - datetime.timedelta(
        days=91
    )
    transactions_by_category = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= picked_data)
        & (
            pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
            >= earlier_data
        )
        & (df_transactions["Категория"] == category)
    ]

    return transactions_by_category


if __name__ == "__main__":
    result = spending_by_category(
        reading_excel("..\\data\\operations.xlsx"),
        "Супермаркеты",
        "01.01.2021 00:00:00",
    )
    print(result)
