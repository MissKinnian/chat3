"""chatserver lib"""

from itertools import cycle


def xor(message, key):
    """encrypt message"""

    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(key)))


class LCG:  # pylint: disable=too-few-public-methods
    """https://stackoverflow.com/a/9024521/8326867"""

    def __init__(self, seed=1):
        self.state = seed

    def random(self):
        """generate next random"""

        self.state = (1103515245 * self.state + 12345) % (2**31)
        return self.state
