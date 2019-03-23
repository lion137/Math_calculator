# Data Structures, enviroment, ...

import math

operands = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01"
operands_bin = "01"
bin_opers = ["&&", "||", "=>", "<=>"]
unary_op = ["~"]
bin_opers_math = ["&", "|", "^", "%", "**", "+", "-", "*", "/", "//", ">>", "<<"]
unary_opers_math = ["UM"]
CONSTANTS = ["pi", "e"]
functions_math = [
    "acos",
    "acosh",
    "asin",
    "asinh",
    "atan",
    "atan2",
    "atanh",
    "ceil",
    "copysign",
    "cos",
    "cosh",
    "degrees",
    "erf",
    "erfc",
    "exp",
    "expm1",
    "fabs",
    "factorial",
    "floor",
    "fmod",
    "frexp",
    "fsum",
    "gamma",
    "gcd",
    "hypot",
    "isclose",
    "isfinite",
    "isinf",
    "isnan",
    "ldexp",
    "lgamma",
    "log",
    "log1p",
    "log10",
    "log2",
    "modf",
    "pow",
    "radians",
    "sin",
    "sinh",
    "sqrt",
    "tan",
    "tanh",
    "trunc",
]

env = {}

env.update(vars(math))

AND = lambda x, y: x and y
OR = lambda x, y: x or y
IFT = lambda x, y: (not x) or y
IFO = lambda x, y: not XOR(x, y)

NOT = lambda x: not x

env.update({"&&": AND, "||": OR, "=>": IFT, "<=>": IFO, "~": NOT})


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        t = self.stack[-1]
        self.stack.pop()
        return t

    def size(self):
        return len(self.stack)

    def isEmpty(self):
        return self.size() == 0

    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self.stack)

    def peek(self):
        return self.stack[-1]

    def __eq__(self, other):
        return self.stack == other.stack
