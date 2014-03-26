# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

import ast
import re
from piescript.pyjson import Literal, dumps

HANDLERS = {}
INDENT_EXP = re.compile('(^|\n)')

OPERATOR_MAP = {
    ast.Add: Literal('__.pyOpAdd'),
}


def compile(string, filename='<unknown>'):
    t = ast.parse(string, filename)
    return handle(t, set())


def var_statement(scope):
    if len(scope) > 0:
        return Literal("var {};\n".format(", ".join(scope)))
    else:
        return Literal("")


def indent(s, i='    '):
    if len(s) > 0 and s != ';':
        return Literal(INDENT_EXP.sub(r'\n' + i, s) + '\n', noexpand=True)
    else:
        return Literal('')


def handle(node, scope):
    try:
        return HANDLERS[node.__class__](node, scope)
    except KeyError:
        raise NotImplementedError('Trying to convert a {} node I can\'t understand!'.format(
            node.__class__,
        ))


def handle_module(node, scope):
    body = Literal("\n".join(handle(x, scope) for x in node.body), noexpand=True)

    return Literal(
        "{}{}\n",
        var_statement(scope),
        body,
    )

HANDLERS[ast.Module] = handle_module


def handle_num(node, scope):
    if isinstance(node.n, int):
        return Literal("__.pyInt({})", node.n)
    else:
        return Literal("__.pyFloat({})", node.n)

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

        return Literal(dumps(js_args)), Literal(", ".join(names))

    sub_scope = set()
    scope.add(node.name)
    js_args, names = build_args(node.args)
    body = "\n".join(handle(x, sub_scope) + ';' for x in node.body)

    return Literal(
        "{} = __.pyFunction({}, function ({}) {{{}}});",
        Literal(node.name),
        js_args,
        names,
        indent(Literal(
            '{}{}',
            var_statement(sub_scope - set(names)),
            Literal(body, noexpand=True),
        )),
    )

HANDLERS[ast.FunctionDef] = handle_function_def


def handle_return(node, scope):
    value = handle(node.value, scope)
    return Literal('return {}', value)

HANDLERS[ast.Return] = handle_return


def handle_bin_op(node, scope):
    op_class = node.op.__class__

    if op_class not in OPERATOR_MAP:
        raise NotImplementedError('Operator {} is not handled yet'.format(op_class))

    return Literal(
        "{}({}, {})",
        OPERATOR_MAP[op_class],
        handle(node.left, scope),
        handle(node.right, scope),
    )

HANDLERS[ast.BinOp] = handle_bin_op


def handle_name(node, scope):
    scope.add(node.id)
    return Literal(node.id)

HANDLERS[ast.Name] = handle_name


def handle_pass(node, scope):
    return Literal("")

HANDLERS[ast.Pass] = handle_pass


def handle_assign(node, scope):
    def assign_one(target):
        return Literal('{} = {}', handle(target, scope), handle(node.value, scope))

    return Literal("\n".join(assign_one(t) for t in node.targets), noexpand=True)

HANDLERS[ast.Assign] = handle_assign
