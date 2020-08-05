
import re

from MagicError import *

class MagicInput(object):
    def __init__(self, input):
        # serialize input
        self.input = input.replace("÷", "/").replace("×", "*").replace(" ", "")

        # TODO replace functions with single character

        self.ops = ["*", "/", "+", "/", "mod"]
        self.signs = ["+", "-"]
        self.funcs = ["sin", "cos", "tan", "sinh", "cosh", "tanh"]

    def validate(self):
        input = self.input

        try:
            l = 0
            is_opened = False
            is_op = False
            is_sign = False
            is_sign_used = False
            is_dot = False
            is_dot_used = False
            is_per = False

            for c in input:
                # decimal
                if is_dot: 
                    # ..
                    if c == "." or is_dot_used:
                        raise DecimalError
                    # .*, ./, .+, .(, .%
                    if c in self.ops or c == "(" or c == "%":
                        raise DecimalError
                    else:
                        # 23.84.57
                        is_dot_used = True

                # operator
                if is_op:
                    # /*, **, ^^ 
                    if c in self.ops and c not in self.signs:
                        raise OperatorError
                    is_dot_used = False

                # percentage, %%, %34, %.
                if is_per and (c == "%" or c.isnumeric or c == "."):
                    raise PercentSignError

                # parentheses
                if c == "(":
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
                is_op = c in self.ops
                is_sign = c in self.signs
                is_per = c == "%"

            # mismatch left, end of string
            if l > 0:
                raise ParenthesisError

            return ""
        except DecimalError:
            return "Decimal Error"
        except OperatorError:
            return "Invalid Operation"
        except PercentSignError:
            return "Misplaced Percentage"
        except ParenthesisError:
            return "Malformed Expression"

        # pattern = re.compile(r'^\(*[0-9]+[\(\)]*([\+\-\*\/\^]?[\(\)]*[0-9]+[\(\)]*)*$')
        # return ""

        # pattern = re.compile(r'^\(*(\d+(?:\.\d+)?)\%?[\(\)]*([\+\-\*\/\^]?[\(\)]*(\d+(?:\.\d+)?)\%?[\(\)]*)*$')
        # matches = pattern.finditer(input)
        
        # try:
        #     if(input.count("(") != input.count(")")):
        #         raise ParenthesisError

        #     match = next(matches).group()

        #     if(match == input or len(input) == 0):
        #         return ""
        #     else:
        #         return "Invalid Input"
        # except ParenthesisError:
        #     return "Malformed Expression"
        # except StopIteration:
        #     return "Invalid Input"
