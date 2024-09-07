import json
import logging
import re

from src.utils import get_dict_transaction

logger_utils = logging.getLogger("utils")
service_handler = logging.FileHandler("../logs/service.log", "w", encoding="utf-8")
service_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
service_handler.setFormatter(service_formatter)
logger_utils.addHandler(service_handler)
logger_utils.setLevel(logging.DEBUG)


def get_transactions_excel(excel_path: list[dict]) -> list[dict]:
    """принимает на вход путь до файла Excel и возвращает список транзакций"""
    transaction_list = []
    trans_pattern = r"\b[А-Я][а-я]+\s[А-Я]\."
    logger_utils.info("Считываю информацию...")
    for e_data in excel_path:
        if "Описание" in e_data and re.match(trans_pattern, e_data["Описание"]):
            transaction_list.append(e_data)
    if transaction_list:
        logger_utils.info("Файлы найдены и отфильтрованы!")
        list_to_json = json.dumps(transaction_list, ensure_ascii=False)
        logger_utils.info("Вот список:")
        return list_to_json
    else:
        logger_utils.critical("Файл не найден")
        return None


if __name__ == "__main__":
    result = get_transactions_excel(get_dict_transaction("..\\data\\operations.xlsx"))
    print(result)
