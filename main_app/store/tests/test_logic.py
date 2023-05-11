from django.test import TestCase
from store.logic import calc



class LogicTestCase(TestCase):
    def test_plus(self):
        res = calc(6, 7, '+')
        self.assertEqual(13, res)
    def test_minus(self):
        res = calc(10, 7, '-')
        self.assertEqual(3, res)
    def test_mult(self):
        res = calc(5, 4, '*')
        self.assertEqual(20, res)
