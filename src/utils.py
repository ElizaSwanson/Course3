import os
import pandas as pd
import json
import logging

path_to_log = "logs/utils.log"
abs_path = os.path.abspath(path_to_log)


logger_utils = logging.getLogger("utils")
utils_handler = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
utils_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
utils_handler.setFormatter(utils_formatter)
logger_utils.addHandler(utils_handler)
logger_utils.setLevel(logging.DEBUG)


def reading_excel(path_to_file: str) -> list[dict]:
    try:
        df_list = pd.read_excel(path_to_file)
        return df_list
    except FileNotFoundError:
        raise

def get_dict_transaction(file_path) -> list[dict]:
    """Функция преобразовывающая датафрейм в словарь pyhton"""
    logger_utils.info(f"Вызвана функция get_dict_transaction с файлом {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger_utils.info(f"Файл {file_path}  прочитан")
        dict_transaction = df.to_dict(orient="records")
        logger_utils.info("Датафрейм  преобразован в список словарей")
        return dict_transaction
    except FileNotFoundError:
        logger_utils.error(f"Файл {file_path} не найден")
        raise
    except Exception as e:
        logger_utils.error(f"Произошла ошибка: {str(e)}")
        raise
