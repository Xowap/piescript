# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

import json as _json
from json import encoder as _encoder
from json import *

_real_encode_basestring = _encoder.encode_basestring
_real_encode_basestring_ascii = _encoder.encode_basestring_ascii


class Literal(str):
    # noinspection PyArgumentList
    def __new__(cls, tpl, *args, **kwargs):
        return str.__new__(cls, _render_literal(tpl, *args, **kwargs))


class JSONPyEncoder(JSONEncoder):
    pass


def dumps(*args, **kwargs):
    kwargs['cls'] = JSONPyEncoder
    return _json.dumps(*args, **kwargs)


def _render_literal(tpl, *args, **kwargs):
    args = [dumps(arg) for arg in args]
    kwargs = dict((name, dumps(arg)) for name, arg in kwargs.items())
    return tpl.format(*args, **kwargs)


def _pyjson_encode_basestring(s):
    if isinstance(s, Literal):
        return s
    else:
        return _real_encode_basestring(s)


def _pyjson_encode_basestring_ascii(s):
    if isinstance(s, Literal):
        return s
    else:
        return _real_encode_basestring_ascii(s)


_encoder.encode_basestring = _pyjson_encode_basestring
_encoder.encode_basestring_ascii = _pyjson_encode_basestring_ascii
