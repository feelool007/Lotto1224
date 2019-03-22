import unittest

from utils import oddAndEven, smallAndLarge

class TestOddAndEven(unittest.TestCase):

    def test_7odd_and_5even(self):
        result = oddAndEven([
            "01", "03", "05", "07", "09", "11",
            "15", "02", "04", "06", "08", "10"
        ])
        self.assertEqual(result, "7單5雙")

    def test_12odd_and_0event(self):
        result = oddAndEven([
            "01", "03", "05", "07", "09", "11",
            "13", "15", "17", "19", "21", "23"
        ])
        self.assertEqual(result, "12單0雙")

    def test_0odd_and_12event(self):
        result = oddAndEven([
            "02", "04", "06", "08", "10", "12",
            "14", "16", "18", "12", "22", "24"
        ])
        self.assertEqual(result, "0單12雙")

class TestSmallAndLarge(unittest.TestCase):

    def test_5small_and_7large(self):
        result = smallAndLarge([
            "01", "02", "03", "04", "05", "13",
            "14", "15", "16", "17", "18", "19"
        ])
        self.assertEqual(result, "5小7大")

    def test_12small_and_0large(self):
        result = smallAndLarge([
            "01", "02", "03", "04", "05", "06",
            "07", "08", "09", "10", "11", "12"
        ])
        self.assertEqual(result, "12小0大")

    def test_0small_and_12large(self):
        result = smallAndLarge([
            "13", "14", "15", "16", "17", "18",
            "19", "20", "21", "22", "23", "24"
        ])
        self.assertEqual(result, "0小12大")

if __name__ == '__main__':
    unittest.main()
