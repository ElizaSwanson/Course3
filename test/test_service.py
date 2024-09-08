import json

import pytest

from src.service import get_transactions_excel


@pytest.fixture
def trans_test():
    return [{"Описание": "Стародубцева Е."}, {"Описание": "Снятие наличных"}]


@pytest.fixture
def trans_test_NO_NEEDED_INFO():
    return [{"Описание": "Каршеринг"}]


def test_one_transaction(trans_test):
    res = get_transactions_excel(trans_test)
    expected = json.dumps(
        [{"Описание": "Стародубцева Е."}], ensure_ascii=False, indent=4
    )
    assert res == expected


def test_no_trans(trans_test_NO_NEEDED_INFO):
    res = get_transactions_excel(trans_test_NO_NEEDED_INFO)
    expect = json.dumps([])
    assert res == expect


def test_no_data():
    res = get_transactions_excel([])
    exp = "[]"
    assert res == exp


@pytest.mark.parametrize(
    "trans, expected",
    [
        (
            [
                {"Описание": "Перевод Ф."},
                {"Описание": "Оплата услуги"},
                {"Описание": "Перевод физлицу на сумму 1000"},
            ],
            json.dumps(
                [
                    {"Описание": "Перевод Ф."},
                ],
                ensure_ascii=False,
                indent=4,
            ),
        )
    ],
)
def test_get_transactions_fizlicam(trans, expected):

    result = get_transactions_excel(trans)

    assert result == expected


if __name__ == "__main__":
    pytest.main()
