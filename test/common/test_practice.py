from time import sleep
from test.common.AeMSCase import AeMSCase
from utils.common.UTX import tag, Tag


class Test(AeMSCase):

    @tag(Tag.LOW, Tag.SMOKE)
    def test_a_method(self):
        sleep(0.25)
        print(1)

    @tag(Tag.MEDIUM)
    def test_c_method(self):
        sleep(0.25)
        print(3)

    @tag(Tag.LOW, Tag.HIGH)
    def test_b_method(self):
        sleep(0.25)
        self.assertEqual(2 + 2, 3)


