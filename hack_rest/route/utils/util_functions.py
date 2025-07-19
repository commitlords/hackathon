import re


def camel_to_snake_case(camel_str):
    # Inserts an underscore before any uppercase letter that is preceded by
    # a lowercase letter or digit,
    # then converts the entire string to lowercase.
    s1 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", camel_str)
    return s1.lower()
