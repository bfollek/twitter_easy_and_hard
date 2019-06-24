import random
import string


class RandomString:
    @staticmethod
    def get(size=16, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for x in range(size))
