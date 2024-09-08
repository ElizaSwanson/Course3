from src.utils import get_user_setting, reading_excel
from src.views import main_window

if __name__ == "__main__":
    transactions = reading_excel("..\\data\\operations.xlsx")
    date = "25.04.2020 11:11:11"

    user_currencies, user_stocks = get_user_setting("..\\user_settings.json")

    main_w_test = main_window(transactions, date, user_currencies, user_stocks)
    print(main_w_test)
