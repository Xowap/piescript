/*vim: fileencoding=utf8 tw=100 expandtab ts=4 sw=4 */
/*jslint indent: 4, maxlen: 100 */
/*global exports */

(function (exports) {
    'use strict';

    var exceptions;

    var PyInt;

    var makeException,
        makeArgs,
        pyFunction,
        pyInt,
        pyOpAdd;

    makeException = function (name, defaultMessage) {
        return new Function('message', 'this.constructor.prototype.__proto__ = Error.prototype;\n' +
            'Error.captureStackTrace(this, this.constructor);\n' +
            'this.name = this.constructor.name;\n' +
            'this.message = message || ' + JSON.stringify((defaultMessage)) + ';');
    };

    makeArgs = function (args) {
        return {
            args: args
        };
    };

    pyFunction = function (argsDesc, func) {
        return function (args) {
            var realArgs = [], type, name, def, i;

            for (i = 0; i < argsDesc.length; i += 1) {
                type = argsDesc[i][0];
                name = argsDesc[i][1];
                def = argsDesc[i][2];

                if (type === '') {
                    if (args.args.length > 0) {
                        realArgs.push(args.args.shift());
                    } else if (def !== undefined) {
                        realArgs.push(def);
                    } else {
                        throw new exceptions.TypeError('Missing at least positional argument "'
                            + name + '"');
                    }
                }
            }

            return func.apply(this, realArgs);
        }
    };

    PyInt = function (number) {
        var that = this,
            py___add__;

        py___add__ = pyFunction([
            ['', 'self', undefined],
            ['', 'other', undefined]
        ], function (self, other) {
            return pyNumber(self.value + other.value);
        });

        that.value = number;
        that.py___class__ = {py___name__: 'int'}
        that.py___add__ = py___add__;
    };

    pyInt = function (number) {
        return new PyInt(number);
    };

    pyOpAdd = function (a, b) {
        if (a.hasOwnProperty('py___add__')) {
            return a.py___add__(makeArgs(a, b));
        } else {
            throw new exceptions.NotImplementedError('Type ' + a.py___class__.py___name__ +
                ' does not implement addition.');
        }
    };

    exceptions = {
        'SyntaxError': makeException('SyntaxError', 'Something you wrote is sooo wrong'),
        'TypeError': makeException('TypeError', 'You\'re using that type incorrectly bro'),
        'NotImplementedError': makeException('NotImplementedError', 'This feature is not ' +
            'implemented')
    };

    exports.exceptions = exceptions;

    exports.makeArgs = makeArgs;
    exports.pyFunction = pyFunction;
    exports.pyInt = pyInt;
    exports.pyOpAdd = pyOpAdd;
}(exports));
