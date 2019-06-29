import random
import string


class RandomString:
    """
    From https://pythontips.com/2013/07/28/generating-a-random-string/
    """

    @staticmethod
    def make(size=32, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for x in range(size))
