from business.price_action import calculator


def convert_to_heikin_ashi(price):
    price = calculator.normalize_price(price)
    return price

