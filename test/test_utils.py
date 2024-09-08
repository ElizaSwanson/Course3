import datetime
import datetime as dt
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import (get_data, get_dict_transaction, get_expenses_cards,
                       get_greeting, reading_excel)


def test_get_data_input():
    input_data = "29.04.2024 11:11:11"
    expected_output = datetime.datetime(2024, 4, 29, 11, 11, 11)
    assert get_data(input_data) == expected_output


def test_reader_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        reading_excel("idkwispath")


def test_get_dict_transaction_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_dict_transaction("idkwispath")


def test_get_greeting_morning():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2024, 4, 29, 11, 11, 11)
            assert get_greeting() == "Доброе утро"


def test_get_greeting_afternoon():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2024, 4, 29, 13, 13, 13)
            assert get_greeting() == "Добрый день"


def test_get_greeting_evening():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2024, 4, 29, 22, 22, 22)
            assert get_greeting() == "Добрый вечер"


def test_get_greeting_night():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 23, 0, 0)
            assert get_greeting() == "Доброй ночи"


@pytest.fixture
def sample_trans():
    return pd.DataFrame(
        {"Номер карты": ["*4444", "*5058"], "Сумма платежа": [-500, -1313]}
    )


def test_get_expenses_cards(sample_trans):
    result = get_expenses_cards(sample_trans)

    assert result[0] == {"last_digits": "*4444", "total spent": 500, "cashback": 5}
    assert result[1] == {"last_digits": "*5058", "total spent": 1313, "cashback": 13}


if __name__ == "__main__":
    pytest.main()
