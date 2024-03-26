import random
import string


def get_dummy_string_for_email_address(prefix: str):
    number_part = random.randint(100, 999)  # Ensures 3 digits (inclusive)
    # Generate 3 random lowercase letters
    letters_part = ''.join(random.choices(string.ascii_lowercase, k=3))
    # Combine the number and letters
    random_string = prefix + '_dummy_' + str(number_part) + letters_part + '@themartec.com'
    return random_string


def get_random_string():
    # Generate the 3-digit number
    number_part = random.randint(100, 999)  # Ensures 3 digits (inclusive)
    # Generate 3 random lowercase letters
    letters_part = ''.join(random.choices(string.ascii_lowercase, k=3))
    # Combine the number and letters
    random_string = str(number_part) + letters_part
    return random_string
