# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from piescript.pyjson import *
import unittest


class TestJson(unittest.TestCase):
    def test_encode_simple_literal(self):
        literal = Literal('undefined')
        output = dumps(literal)

        self.assertEqual('undefined', output)

    def test_encode_in_object(self):
        literal = Literal('undefined')
        output = dumps({
            'test': literal
        })

        self.assertEqual('{"test": undefined}', output)
