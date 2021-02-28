def is_digit(s):
    return str(s).lstrip('-').replace('.', '').isdigit()
