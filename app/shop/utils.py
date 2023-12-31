import random
import string


def random_slug():
    """
    Generates a random slug consisting of a combination of three letters and digits.
    Returns:
        str: The randomly generated slug.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))