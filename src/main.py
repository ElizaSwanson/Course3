from src.utils import reading_excel, get_user_setting, get_currency_rates, get_stock_price
from src.views import main_window
from src.views import get_expenses_cards, get_greeting, top_transaction, transaction_currency


if __name__ == "__main__":
    transactions = reading_excel("..\\data\\operations.xlsx")
    date = "25.04.2020 11:11:11"

    user_currencies, user_stocks = get_user_setting("..\\user_settings.json")

    main_w_test = main_window(transactions, date, user_currencies, user_stocks)
    print(main_w_test)