import json

from src.utils import (get_currency_rates, get_expenses_cards, get_greeting,
                       get_stock_price, top_transaction)


def main_window(transactions, date, currencies, stocks):
    """функция-"обложка" приложения"""

    greeting = get_greeting()
    cards_info = get_expenses_cards(transactions)
    top_transatcs = top_transaction(transactions)
    rates = get_currency_rates(currencies)
    stock_info = get_stock_price(stocks)
    json_response = json.dumps(
        {
            "greeting": greeting,
            "cards": cards_info,
            "top purchases": top_transatcs,
            "currency rates": rates,
            "stock prices": stock_info,
        },
        indent=4,
        ensure_ascii=False,
    )
    return json_response
