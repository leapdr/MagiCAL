
import re

from MagicError import *

TOSYMBOL = {
    "*": "×",
    "/": "÷"
}

SIGNS = ["+", "-"]
OPS = ["*", "/", "+", "-", "m"]
FUNCS = ["s", "S", "c", "C", "t", "T"]

class MagicInput(object):
    def __init__(self, input):
        # serialize input
        if type(input) != str:
            input = str(input)

        self.input = input.replace("÷", "/").replace("×", "*").replace(" ", "").replace("mod", "m").replace("sin", "s").replace("sinH", "S").replace("cos", "c").replace("cosh", "C").replace("tan", "t").replace("tanh", "T")

    def isInteger(self):
        return self.input.isnumeric()

    def validate(self):
        input = self.input

        try:
            l = 0

            # init flags
            is_opened = is_op = is_sign = is_dot = is_dot_used = False
            is_sign_used = is_op_used = is_per = is_func = False

            i = 0
            for c in input:
                # TODO variables

                # alphabet
                if c.isalpha() and not (c in FUNCS or c in OPS):
                    raise UnrecognizedCharacter

                # decimal
                if is_dot: 
                    # ..
                    if c == "." or is_dot_used:
                        raise DecimalError
                    # .*, ./, .+, .(, .%, .s
                    if c in OPS or c == "(" or c == "%" or c in FUNCS:
                        raise DecimalError
                    else:
                        # 23.84.57
                        is_dot_used = True
                    is_sign_used = is_op_used = False

                # function
                if is_func:
                    # ss - sin sin, cC - cos hyper cos
                    # s*, T/
                    # s%
                    if not c.isnumeric() and c != "(" and c not in SIGNS:
                        raise UnrecognizedFunction
                    # s-+1
                    elif c in SIGNS and input[i+1] in OPS:
                        raise OperatorError(0)
                    is_sign_used = is_op_used = False

                # number
                if c.isnumeric():
                    is_sign_used = is_op_used = False

                # percentage, %%, %34, %.
                if is_per and c not in OPS and c not in SIGNS and c != "(":
                    raise PercentSignError

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

                # assign for next character validation
                is_dot = c == "."
                is_op = c in OPS
                is_sign = c in SIGNS

                # operator and sign
                if is_op:
                    if not is_op_used :
                        # /, * begining of expression
                        if not is_sign and i == 0:
                            raise OperatorError(1)

                        is_op_used = True

                    elif is_sign and not is_sign_used:
                        is_sign_used = True

                    # +x, -/, +++, --*
                    else:
                        raise OperatorError(2)

                    is_dot_used = False

                is_func = c in FUNCS
                is_per = c == "%"

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

        return (terms, ops)
