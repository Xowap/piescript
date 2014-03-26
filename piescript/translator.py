# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

import ast
from piescript.pyjson import Literal, dumps

HANDLERS = {}


def compile(string, filename='<unknown>'):
    t = ast.parse(string, filename)
    return handle(t, set())


def handle(node, scope):
    try:
        return HANDLERS[node.__class__](node, scope)
    except KeyError:
        raise NotImplementedError('Trying to convert a syntax node I can\'t understand!')


def handle_module(node, scope):
    return "\n".join(handle(x, scope) for x in node.body)

HANDLERS[ast.Module] = handle_module


def handle_num(node, scope):
    return Literal("__.pyNumber({})", node.n)

HANDLERS[ast.Num] = handle_num


def handle_function_def(node, scope):
    def build_args(args):
        js_args = []
        names = []

        for arg in args.args:
            js_args.append(['', arg.arg, Literal('undefined')])
            names.append(arg.arg)

        offset = len(js_args) - len(args.defaults)
        for i in range(0, len(args.defaults)):
            js_args[offset + i][-1] = handle(args.defaults[-i], scope)

        return Literal(dumps(js_args)), names

    scope.add(node.name)

    return Literal("pyFunction({}, function({}) {{ {} }}", *(build_args(node.args) + (Literal(''),)))

HANDLERS[ast.FunctionDef] = handle_function_def
