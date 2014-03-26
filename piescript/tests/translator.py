# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from unittest import TestCase
from piescript import translator


class TestTranslator(TestCase):
    def test_simple_function(self):
        code = """
def add(a, b):
    return a + b
"""

        expected = "pyFunction([[\"\", \"a\", undefined], [\"\", \"b\", undefined]], " \
                   "function(a, b) {  }"

        self.assertEqual(expected, translator.compile(code))

    def test_simple_function_with_default(self):
        code = """
def add(a, b=1, c=2):
    pass
"""

        expected = "pyFunction([[\"\", \"a\", undefined], [\"\", \"b\", __.pyNumber(1)], " \
                   "[\"\", \"c\", __.pyNumber(2)]], function(a, b, c) {  }"

        self.assertEqual(expected, translator.compile(code))
