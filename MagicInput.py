
import re

from MagicError import *

TOSYMBOL = {
    "*": "×",
    "/": "÷"
}

SIGNS = ["+", "-"]
OPS = ["*", "/", "+", "-", "m"]
FUNCS2 = ["a", "s", "S", "c", "C", "t", "T", "l", "L"]
FUNCS = ["abs", "sin", "sinh", "cos", "cosh", "tan", "tanh", "ln", "log"]

class MagicInput(object):
    def __init__(self, input):
        # serialize input
        if type(input) != str:
            input = str(input)

        self.input = input.replace("÷", "/").replace("×", "*").replace(" ", "").replace("mod", "m")

    def isInteger(self):
        return self.input.isnumeric()

    def validate(self):
        input = self.input

        print(input)

        try:
            l = 0

            # init flags
            is_opened = False
            is_op = False
            is_sign = False
            is_dot = False
            is_per = False
            is_func = False
            is_alpha = False
            is_num = False
            is_sign_used = False
            is_op_used = False
            is_dot_used = False

            i = 0
            fn = p = ""
            f = 0
            for c in input:
                if p == "":
                    p = c

                    # assign
                    is_op = p in OPS
                    is_sign = p in SIGNS

                    # illegal start of expression
                    if is_op and not is_sign:
                        raise OperatorError(1)
                else:
                    # print(p)
                    # print(f"is op {is_op}")
                    # print(f"is sign {is_sign}")
                    # print(f"is dot {is_dot}")
                    # print(f"is per {is_per}")
                    # print(f"is alpha {is_alpha}")
                    # print(f"is num {is_num}")
                    # print()

                    is_op = c in OPS
                    is_sign = c in SIGNS
                    is_dot = c == "."
                    is_per = c == "%"
                    is_alpha = c.isalpha()
                    is_num = c.isnumeric()

                    n = ""
                    if i + 1 < len(input):
                        n = input[i+1]

                    # number
                    if is_num:
                        if p.isalpha() and fn not in FUNCS and fn not in OPS:
                            raise UnrecognizedCharacter
                        elif p == "%":
                            raise PercentSignError
                        fn = ""
                        is_op_used = False

                    # function, alphabet
                    elif is_alpha:
                        fn += c

                        if p == "%":
                            raise PercentSignError
                        elif p == ")":
                            raise ParenthesisError
                        elif p == ".":
                            raise DecimalError
                        is_op_used = False

                    # decimal point / dot
                    elif is_dot:
                        if is_dot_used or p == ".":
                            raise DecimalError
                        is_op_used = False

                    # percent
                    elif is_per:
                        alp = p.isalpha()
                        if alp or p == "." or p in OPS:
                            raise PercentSignError

                    # operators
                    elif is_op:
                        alp = p.isalpha()
                        if p == ".":
                            raise DecimalError
                        elif alp and p not in OPS:
                            raise OperatorError(2)
                        elif p in OPS:
                            if p not in SIGNS or (p in SIGNS and is_sign_used):
                                raise OperatorError(2)

                        if not is_op_used:
                            is_op_used = True
                        elif c in SIGNS and not is_sign_used:
                            is_sign_used = True

                        is_dot_used = False

                    # parentheses
                    if c == "(":
                        is_sign_used = is_op_used = False
                        l += 1
                        is_opened = True
                    elif c == ")":
                        # ()
                        if is_opened:
                            raise ParenthesisError
                        l -= 1
                    else:
                        is_opened = False

                    # mismatch right, terminate loop
                    if l < 0:
                        raise ParenthesisError

                    p = c

                i += 1

            # mismatch left, end of string
            if l > 0:
                raise ParenthesisError
            if is_op_used or is_sign_used:
                raise OperatorError(3)

            return ""
        except DecimalError:
            return "Decimal Error"
        except OperatorError as e:
            return str(e)
        except PercentSignError:
            return "Misplaced Percentage"
        except UnrecognizedCharacter:
            return "Unrecognized Character in Expression"
        except UnrecognizedFunction:
            return "Unrecognized Function or Operation"
        except ParenthesisError:
            return "Malformed Expression"
    
    @staticmethod
    def getTermsAndOps(expr):
        terms = []
        ops = []

        i, t = 0, 0
        is_sign_used = False
        tmp_str = ""

        x = 0
        for c in expr:
            if c in OPS:
                left = not(x != 0 and expr[x-1].isnumeric())
                right = expr[x+1] not in SIGNS

                if c in SIGNS and right and left:
                    tmp_str = tmp_str + c
                else:
                    ops.append(c)
                    terms.append(tmp_str)

                    t += 1
                    tmp_str = ""
                    is_sign_used = False
            else:
                tmp_str = tmp_str + c
            x += 1
        terms.append(tmp_str)

        # print(terms)
        # print(ops)

        return (terms, ops)
