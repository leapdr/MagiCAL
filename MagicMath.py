import sys
import re

from math import *

from MagicError import *
from MagicInput import *

ANGLE_DEFAULT = lambda x: radians(x)

FUNC_EVAL = {
    "s": lambda x: sin(ANGLE_DEFAULT(x)),
    "S": lambda x: sinh(ANGLE_DEFAULT(x)),
    "c": lambda x: cos(ANGLE_DEFAULT(x)),
    "C": lambda x: cosh(ANGLE_DEFAULT(x)),
    "t": lambda x: tan(ANGLE_DEFAULT(x)),
    "T": lambda x: tanh(ANGLE_DEFAULT(x)),
    "a": lambda x: abs(x),
}

class MagicMath(object):
    def __init__(self, interface, input, end=0):
        self.interface = interface
        self.e = input
        self.end = end

    def getInput(self):
        m_input = ""
        if self.interface == "app":
            m_input = MagicInput(self.e.get())
        elif self.interface == "cli":
            m_input = MagicInput(self.e)

        return m_input

    def factorize(self):
        m_input = self.getInput()

        try:
            if not(m_input.isInteger()):
                raise InputError(0)
            elif m_input == "": 
                self.display(0, " to factorize")
            else:
                x = m_input.input
                # convert list item to string
                terms = [str(x) for x in self.getFactors(int(x))]
                self.display(TOSYMBOL["*"].join(terms))
        except OperatorError as e:
            self.display(str(e))

        
    def getFactors(self, x):

        terms = []
        c = 2
        while x != 1:
            if x % c == 0:
                x /= c
                terms.append(c)
                c = 2
            else:
                c += 1
        
        return terms

    def solve(self, o, x, y):
        if(o == "^"):
            return x**y
        elif(o == "/"):
            return x / y
        elif(o == "m"):
            return x % y
        elif(o == "*"):
            return x * y
        elif(o == "-"):
            return x - y
        elif(o == "+"):
            return x + y
        else:
            # or raise an exception
            return "Invalid Operator"

    def assessPrecedence(self, operators):
        highest = 0
        for op in operators:
            if highest == 0 and (op == "+" or op == "-"):
                highest = 1
            elif highest <= 1 and (op == "*" or op == "/" or op == "m"):
                highest = 2
            elif highest <= 2 and (op == "^"):
                highest = 3
            # elif highest <= 3 and (op == "(" or op == ")"):
            #     highest = 4

        self.highest = highest

    def getIndicesMatchingParen(self, input):
        i = 0
        start = 0
        end = 0
        start_found = False
        end_found = False
        start_extra = 0

        while i < len(input) or not(start_found and end_found):
            if input[i] == "(" :
                if not(start_found):
                    start = i
                    start_found = True
                else:
                    start_extra += 1

            if input[i] == ")":
                if start_extra > 0:
                    start_extra -= 1
                else:
                    if not(end_found):
                        end = i
                        end_found = True

            i += 1

        return (start, end)

    def evaluateTerm(self, term):
        term = str(term)

        try:
            # no need term evaluation
            result = float(term)
            return result
        except ValueError:
            # has to be evaluated
            result = 0

            # get decimal value
            p = re.compile(r"([\+\-]?\d*(\.\d+)?)")
            d = list(filter(None, [m.group() for m in p.finditer(term)])).pop()
            i = term.index(d)

            d = float(d)
            # left
            if i-1 >= 0:
                l = term[i-1]
                # function
                if l in FUNCS:
                    result = FUNC_EVAL[l](d)
                else:
                    result = d
            else:
                result = d

            # right
            # percentage
            if term[-1] == "%":
                result /= 100

            return result

    def evaluate(self, input):
        # evaluate parentheses
        paren_count = input.count('(')

        while paren_count > 0:
            # get expression inside parenthesis then evaluate
            indices = self.getIndicesMatchingParen(input)
            start = indices[0] + 1
            end = indices[1]

            exp = input[start:end]

            paren_count -= exp.count('(')
            ans = self.evaluate(exp)

            # replace parenthesis
            paren_converted = False
            char_l, char_r = "", ""
            left = input[start-2]
            less_func = 0

            if left.isnumeric():
                char_l = "*"
                paren_converted = True
            elif left in FUNCS:
                ans = self.evaluateTerm(f"{left}{ans}")
                paren_converted = True
                less_func += 1

            percent_adjust = 0
            if end+1 < len(input):
                if input[end+1].isnumeric():
                    if not(paren_converted):
                        char_r = "*"
                    else:
                        raise ParenthesisError
                elif input[end+1] == "%":
                    ans = self.evaluateTerm(f"{ans}%")
                    percent_adjust = 1

            # restructure input
            input = input[0:start-1-less_func] + char_l + str(ans) + char_r + input[end+1+percent_adjust:]

            paren_count -= 1

        # set the terms and operators
        parts = MagicInput.getTermsAndOps(input)
        terms, operators = parts[0], parts[1]

        # set the operator's highest precedence in the equation
        self.assessPrecedence(operators)

        while len(terms) > 1:
            # evaluate terms with highest operator precedence
            i = 0
            while i < len(operators):
                op = operators[i]

                if(self.precedence[op] == self.highest):

                    # simplify terms
                    x = self.evaluateTerm(terms[i])
                    y = self.evaluateTerm(terms[i+1])

                    res = self.solve(op, x, y)

                    # pop simplified terms and operator in the list
                    terms[i] = res
                    terms.pop(i+1)

                    operators.pop(i)

                    # reassess precedence
                    self.assessPrecedence(operators)

                    # break the loop to restart
                    break

                i += 1

        # evaluate term
        result = self.evaluateTerm(terms[0])

        if result % 1 == 0:
            result = int(result)
        return str(result)

    def display(self, output):
        if self.interface == "app":
            self.e.delete(0, self.end)
            self.e.insert(0, str(output))
        elif self.interface == "cli":
            print(f"{output}")

    def parse(self):
        m_input = self.getInput()

        error = m_input.validate()

        if error == "":
            # initialize precedence for EMDAS
            self.precedence = {
                "^": 3,
                "/": 2,
                "*": 2,
                "m": 2,
                "+": 1,
                "-": 1
            }

            input = m_input.input

            try:
                self.answer = float(self.evaluate(input))
            
                # format float with .0
                if self.answer % 1 == 0:
                    self.answer = int(self.answer)

                # display answer
                self.display(self.answer)
            except ParenthesisError:
                self.display("Malformed Expression")
            except ZeroDivisionError:
                self.display("Division by Zero")

        else:
            self.display(f"{m_input.input}: {error}")