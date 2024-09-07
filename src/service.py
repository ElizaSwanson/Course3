import json
import logging
import re
import pandas as pd
from src.utils import get_dict_transaction


def get_transactions_excel(excel_path: list[dict]) -> list[dict]:
    """принимает на вход путь до файла Excel и возвращает список транзакций"""
    transaction_list = []
    trans_pattern = r"\b[А-Я][а-я]+\s[А-Я]\."
    for e_data in excel_path:
        if "Описание" in e_data and re.match(trans_pattern, e_data["Описание"]):
            transaction_list.append(e_data)
    if transaction_list:
        list_to_json = json.dumps(transaction_list, ensure_ascii=False)
        return list_to_json
    else:
        return None


if __name__ == "__main__":
    result = (get_transactions_excel(get_dict_transaction("..\\data\\operations.xlsx")))
    print(result)


