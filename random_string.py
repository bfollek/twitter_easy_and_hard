import random
import string

# From here: https://pythontips.com/2013/07/28/generating-a-random-string/


class RandomString:
    @staticmethod
    def make(size=32, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for x in range(size))
