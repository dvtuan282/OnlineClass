import random
import string


def ramdomCode():
    char = string.ascii_letters + string.digits
    return ''.join(random.choice(char) for _ in range(8))