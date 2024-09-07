import pytest
import pandas as pd
from src.reports import spending_by_category
from src.utils import get_data


@pytest.fixture
def test_categs():
    """Тестовые данные для функции трат по категориям"""
    data = {
        "Дата операции": [
            "11.11.2019 01:01:01",
            "25.04.2020 19:04:59"
        ],
        "Категория": ["Каршеринг", "Каршеринг"],
        "Сумма операции с округлением": [400, 4192],
    }
    df = pd.DataFrame(data)
    return df


def test_category_with_data(test_categs):
    """Тест с категорией каршеринг, должна возвращаться 1 строка тк за 90 дней была только 1 такая трата"""
    result = spending_by_category(test_categs, "Каршеринг", "11.11.2019 01:01:01")
    assert len(result) == 1


def test_spending_by_category_no_date(test_categs):
    """тест с категорией каршеринг без указания даты, не должно возвращаться ничего"""
    result = spending_by_category(test_categs, "Каршеринг")
    assert len(result) == 0


def test_spending_by_category_future_date(test_categs):
    """тест с датой которая еще не наступила"""
    result = spending_by_category(test_categs, "Каршеринг", "07.09.2024 16:56:55")
    assert len(result) == 0


def test_spending_by_category_no_transactions(test_categs):
    """тест с категорией которая не использовалась"""
    result = spending_by_category(test_categs, "Образование", "11.11.2019 01:01:01")
    assert len(result) == 0


if __name__ == "__main__":
    pytest.main()