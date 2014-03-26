# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from unittest import TestCase
from piescript import translator


class TestTranslator(TestCase):
    def test_simple_function(self):
        code = """
def add(a, b):
    c = 42
    return a + b + c
"""

        expected = """var add;
add = __.pyFunction([["", "a", undefined], ["", "b", undefined]], function (a, b) {
    var c;
    c = __.pyInt(42);
    return __.pyOpAdd(__.pyOpAdd(a, b), c);
});
"""

        self.assertEqual(expected, translator.compile(code))

    def test_simple_function_with_default(self):
        code = """
def add(a, b=1, c=2):
    pass
"""

        expected = """var add;
add = __.pyFunction([["", "a", undefined], ["", "b", __.pyInt(1)], ["", "c", __.pyInt(2)]], function (a, b, c) {});
"""

        self.assertEqual(expected, translator.compile(code))
