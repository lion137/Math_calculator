# tokenize expression

import pdb
import re
from collections import namedtuple

from data import *

control = False
Token = namedtuple("Token", ["type", "value"])

DEF = r"(?P<DEF>def[^a-zA-Z0-9_])"
NAME = r"(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)"

EQI = r"(?P<EQI><=>)"
IMP = r"(?P<IMP>=>)"
OR = r"(?P<OR>\|\|)"
END = r"(?P<END>&&)"
NEG = r"(?P<NEG>~)"
INFR = r"(?P<INFR>\|=)"

SLEFT = r"(?P<SLEFT><<)"
SRIGHT = r"(?P<SRIGHT>>>)"
TDIV = r"(?P<TDIV>\/\/)"
NUM = r"(?P<NUM>\d+)"
POW = r"(?P<POW>\*\*)"
PLUS = r"(?P<PLUS>\+)"
MUL = r"(?P<TIMES>\*)"
DIV = r"(?P<DIV>\/)"
SUB = r"(?P<SUB>\-)"
EQ = r"(?P<EQ>=)"
BXOR = r"(?P<XOR>\^)"
BAND = r"(?P<BAND>&)"
BOR = r"(?P<BOR>\|)"
MOD = r"(?P<MOD>\%)"

WS = r"(?P<WS>\s+)"
LB = r"(?P<LB>\()"
RB = r"(?P<RB>\))"
COMA = r"(?P<COMA>,)"

main_pat = re.compile(
    "|".join(
        [
            DEF,
            NAME,
            EQI,
            IMP,
            OR,
            END,
            NEG,
            INFR,
            SLEFT,
            SRIGHT,
            TDIV,
            NUM,
            POW,
            PLUS,
            MUL,
            DIV,
            SUB,
            EQ,
            BXOR,
            BAND,
            BOR,
            WS,
            LB,
            RB,
            COMA,
        ]
    )
)

# preprocess


def is_proof(v):
    f = lambda x: x == "|="
    if any(map(f, v)):
        return True
    return False


def preprocess_proof(v):
    for i, token in enumerate(v):
        if token == ",":
            v[i] = "&&"
        if token == "|=":
            v[i] = "=>"
    return v


# math formula preporcessing

# is operand check(is name)
def oper_test(st):
    if not re.match("^[a-zA-Z_][a-zA-Z_0-9]*$", st):
        return False
    else:
        return True

#is_digit
def is_digit(st):
	if re.match(r"([^0]\d+\.\d+)|(\d+\.)|([1-9]\d*|0)", st): return True
	else: return False

# parenthesess checks
def bal_parenthesis_check(v):
    st = Stack()
    for t in v:
        if t == "(":
            st.push(t)
        if t == ")":
            if st.isEmpty():
                return False
            else:
                st.pop()
    return st.isEmpty()


# helper to transform_negation_to_unary
def find_index(i, v):
    s = Stack()
    for n, e in enumerate(v[i:]):
        if e == "(":
            s.push("(")
        if e == ")":
            s.pop()
            if s.isEmpty():
                return n + i + 1


# helper to transform
def test_prev(v, i):
    if (
        v[i] == "~"
        and v[i - 1] != ")"
        and not oper_test(v[i - 1])
        or (i == 0 or v[i - 1] == " ")
    ):
        return True
    else:
        return False


def transform_negation_to_unary(v):
    i = 0
    ctrl = 0
    while i < len(v) - 1:
        if v[i] == "~":
            if test_prev(v, i):
                if v[i + 1] == "~":
                    del v[i + 1]
                    del v[i]
                    i -= 1
                    ctrl = 0
                elif oper_test(v[i + 1]):
                    v.insert(i + 2, "~")
                    del v[i]
                    ctrl = 0
                elif v[i + 1] == "(":
                    k = find_index(i + 1, v)
                    v.insert(k, "~")
                    del v[i]
                    ctrl = 0
        if ctrl == 0:
            i += 1
    return v


def parenthesiss_check(v):
    def test(st):
        stack = Stack()
        for e in st:
            if e == "(":
                stack.push(e)
            if e == ")":
                if stack.isEmpty():
                    return False
                else:
                    stack.pop()
                    if stack.isEmpty():
                        return True
        return False

    for i, e in enumerate(v):
        if e == "(":
            if not test(v[i:]):
                return False
    return True


# logical calculus syntax check functions


def after_letter(v):
    lim = len(v)
    for i in range(lim - 1):
        if oper_test(v[i]):
            if v[i + 1] == "(" or v[i + 1] == "~":
                return False
    return True


def after_left_paren(v):
    lim = len(v)
    for i in range(lim - 1):
        if v[i] == "(":
            a = oper_test(v[i + 1])
            b = v[i + 1] == "("
            c = v[i + 1] == "~"
            if not (a or b or c):
                return False
    return True


# operand and operators # check
def operands_operators_number(v):
    bin_opers_cnt = 0
    operands_cnt = 0
    for e in v:
        if oper_test(e):
            operands_cnt += 1
        if e in bin_opers:
            bin_opers_cnt += 1
    return operands_cnt == bin_opers_cnt + 1


def no_operands(v):
    if not any(map(lambda x: re.search("^[a-zA-Z_][a-zA-Z_0-9]*$", x), v)):
        return False
    return True


def syntax_propositional(v):
    b1 = after_left_paren(v)
    b2 = after_letter(v)
    b3 = parenthesiss_check(v)
    b4 = bal_parenthesis_check(v)
    b5 = operands_operators_number(v)
    b6 = no_operands(v)
    b = b1 and b2 and b3 and b4 and b5 and b6
    return b


# general syntax

# is logical formula
def is_propositional(v):
    def helper(st):
        if st in bin_opers or st in unary_op or st == "|=":
            return True
        else:
            return False

    if (len(v) == 1 and oper_test(v[0])) and not re.match("\d+", v[0]):
        return True
    return any(map(helper, v))


def is_math(v):
    def helper(st):
        if st in bin_opers_math:
            return True
        return False

    if len(v) == 1 and re.match("\d+", v[0]):
        return True
    return any(map(helper, v))


def test_prev_math(v, i):
    if (v[i] == "-") and (
        v[i - 1] != ")"
        and not re.match(r"\d+", v[i - 1])
        and not oper_test(v[i - 1])
        or (i == 0)
    ):
        return True
    else:
        return False


def test_prev_math_operator(v, i):
    if (v[i - 1] != ")" and not re.match(r"\d+", v[i - 1]) and not oper_test(v[i - 1])) or i == 0:
        return True
    else:
        return False


def minus_to_unary_math(v):
    i = 0
    ctrl = 0
    while i < len(v) - 1:
        if test_prev_math(v, i):
            if v[i + 1] == "-":
                del v[i + 1]
                del v[i]
                i -= 1
                ctrl = 0
            elif oper_test(v[i + 1]) or re.match(r"\d+", v[i + 1]):
                if i == len(v) - 2 or v[i + 2] != "(":
                    v.insert(i + 2, "-")
                    del v[i]
                    ctrl = 0
                else:
                    k = find_index(i + 1, v)
                    v.insert(k, "-")
                    del v[i]
                    ctrl = 0
            elif v[i + 1] == "(":
                k = find_index(i + 1, v)
                v.insert(k, "-")
                del v[i]
                ctrl = 0
        if ctrl == 0:
            i += 1
    return v


def operator_to_unary_math(v):
    i = 0
    while i < len(v) - 1:
        if v[i] in env.keys() and test_prev_math_operator(v, i):
            k = find_index(i + 1, v)
            v.insert(k, v[i])
            del v[i]
        i += 1
    return v


def syntax_math(v):
    b1 = bal_parenthesis_check(v)
    b2 = parenthesiss_check(v)
    return b1 and b2


####################################################################
def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


def tokenize(expr):
    if expr == "" or re.match("\\s+", expr):
        return 2, []
    tokens = []
    for tok in generate_tokens(main_pat, expr):
        if tok.type != "WS":
            tokens.append(tok.value)
    if is_propositional(tokens):
        if is_proof(tokens):
            tokens = preprocess_proof(tokens)
            global control
            control = 1
        else:
            control = 0
        if not syntax_propositional(tokens):
            return None, "Syntax Error"
        return control, transform_negation_to_unary(tokens)
    if is_math(tokens):
        if syntax_math(tokens):
            tokens = minus_to_unary_math(tokens)
            tokens = operator_to_unary_math(tokens)
            return 2, tokens
        else:
            return None, "Syntax Error"
    else:
        return None, "Syntax Error"


class Eval:
    def __init__(self, v):
        self.logic_ctrl, self.tokens = tokenize(v)

    def eval(self):
        if self.logic_ctrl is not None:
            if self.logic_ctrl < 2:
                return self.__parser_propositional(self.tokens)
            else:
                return self.__parser_math(self.tokens)
        else:
            return "Sorry, I don't understand'"

    def __parser_math(self, v):
        prec = {}
        prec.fromkeys(functions_math, 10)
        prec["**"] = 9
        prec["UM"] = 8
        prec["*"]  = 7
        prec["/"]  = 7
        prec["//"] = 7
        prec["%"]  = 7
        prec["+"]  = 6
        prec["-"]  = 6
        prec[">>"] = 5
        prec["<<"] = 5
        prec["&"]  = 4
        prec["^"]  = 3
        prec["|"]  = 2
        prec["("]  = 1
        op_stack = Stack()
        postfix_list = []
        for token in v:
            if is_digit(token) or token in CONSTANS:
                postfix_list.append(token)
            elif token == "(":
                op_stack.push(token)
            elif token == ")":
                top = op_stack.pop()
                while top != "(":
                    postfix_list.append(top)
                    top = op_stack.pop()
            else:
                while (not op_stack.isEmpty()) and (
                    prec[op_stack.peek()] >= prec[token]
                ):
                    postfix_list.append(op_stack.pop())
                op_stack.push(token)

        while not op_stack.isEmpty():
            postfix_list.append(op_stack.pop())
        return postfix_list
        
    def __parser_propositional(self, v):
        prec = {}
        prec["~"] = 6
        prec["&&"] = 5
        prec["||"] = 4
        prec["<=>"] = 3
        prec["=>"] = 2
        prec["("] = 1
        op_stack = Stack()
        postfix_list = []
        for token in v:
            if oper_test(token):
                postfix_list.append(token)
            elif token == "(":
                op_stack.push(token)
            elif token == ")":
                top = op_stack.pop()
                while top != "(":
                    postfix_list.append(top)
                    top = op_stack.pop()
            else:
                while (not op_stack.isEmpty()) and (
                    prec[op_stack.peek()] >= prec[token]
                ):
                    postfix_list.append(op_stack.pop())
                op_stack.push(token)

        while not op_stack.isEmpty():
            postfix_list.append(op_stack.pop())
        return postfix_list

    def __repr__(self):
        return str(self.logic_ctrl) + ", " + str(self.tokens)

    def __sat(self):
        self.tokens.insert(0, "(")
        self.tokens.insert(0, "~")
        self.tokens.append(")")
        return self.tokens


if __name__ == "__main__":
    assert tokenize("-log(-log(-1))")[1] == [
        "(",
        "(",
        "1",
        "-",
        ")",
        "log",
        "-",
        ")",
        "log",
        "-",
    ]
    assert tokenize("-sin(--1)* -(-(-1))")[1] == [
        "(",
        "1",
        ")",
        "sin",
        "-",
        "*",
        "(",
        "(",
        "1",
        "-",
        ")",
        "-",
        ")",
        "-",
    ]
    assert tokenize("----1")[1] == ["1"]
    assert tokenize("-sin(-1)*-----1")[1] == [
        "(",
        "1",
        "-",
        ")",
        "sin",
        "-",
        "*",
        "1",
        "-",
    ]
    assert tokenize("-log(-1 * --2)")[1] == ["(", "1", "-", "*", "2", ")", "log", "-"]
    assert tokenize("-(-1 * - -2)")[1] == ["(", "1", "-", "*", "2", ")", "-"]

    assert tokenize("Q + --2")[1] == ["Q", "+", "2"]
    assert tokenize("2 >> 3")[1] == ["2", ">>", "3"]
    assert tokenize("2 // 3")[1] == ["2", "//", "3"]
    assert tokenize("2 << 3 << a")[1] == ["2", "<<", "3", "<<", "a"]
    assert tokenize("")[1] == []
    assert tokenize("A + A")[1] == ["A", "+", "A"]
    assert is_propositional(tokenize("~A || B")[1]) is True
    assert is_propositional(tokenize("A1")[1]) is True
    assert is_propositional(tokenize("A1, A2 |= ~D")[1]) is True
    assert tokenize("A, Q |= ~AS")[1] == ["A", "&&", "Q", "=>", "AS", "~"]
    assert tokenize("A |= A")[1] == ["A", "=>", "A"]
    assert is_proof(["A", "|=", "A"]) is True
    assert is_proof(["A", "="]) is False
    assert tokenize("~ A => B1")[1] == ["A", "~", "=>", "B1"]
    assert tokenize("~ ")[1] == "Syntax Error"
    assert tokenize("~~ => A")[1] == "Syntax Error"
    assert tokenize("Q || Q")[1] == ["Q", "||", "Q"]
    assert tokenize("~~~~cd => A")[1] == ["cd", "=>", "A"]
    assert tokenize("~(~A&&~(C ||D))")[1] == [
        "(",
        "A",
        "~",
        "&&",
        "(",
        "C",
        "||",
        "D",
        ")",
        "~",
        ")",
        "~",
    ]

    print("Test Passed")
    print(tokenize("A |= A")[0])
