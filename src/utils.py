import datetime
import logging
import os

import pandas as pd

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
