from random import randint
import string

def post_id():
    result = ""

    for i in range(8): result += string.ascii_lowercase[randint(0, 25)]

    return result

def comment_id():
    result = ""

    for i in range(8): result += str(randint(0, 9))

    return result

