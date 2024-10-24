import random
import string


def gen_random_string(len_string):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=len_string))
