import unittest
from lm import LM


class TestLM(unittest.TestCase):
    def setUp(self):
        self.model = LM()

    def test_predict(self):
        print(self.model.predict())


if __name__ == "__main__":
    unittest.main()
