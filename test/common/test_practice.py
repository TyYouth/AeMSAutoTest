from time import sleep

from utils.common.UTX import TestCase, tag, Tag
from test.common.AeMSCase import AeMSCase

class Test(AeMSCase):

    def test_a_method(self):
        sleep(0.25)
        print(1)

    @tag(Tag.MEDIUM)
    def test_c_method(self):
        sleep(0.25)
        print(3)

    @tag(Tag.HIGH)
    def test_b_method(self):
        sleep(0.25)
        self.assertEqual(2 + 2, 3)


