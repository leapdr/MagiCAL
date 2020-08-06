import sys
import re

from MagicError import *
from MagicInput import *

class MagicMath(object):
    def __init__(self, interface, input, end=0):
        self.interface = interface
        self.e = input
        self.end = end

    def getPercent(self, term):
        term = str(term)
        result = 0

        if term.find("%") and term[-1] == "%":
            result = term[0:-1]
            result = float(result) / 100
        else:
            result = float(term)

        return result

    def solve(self, o, x, y):
        if(o == "^"):
            return x**y
        elif(o == "/"):
            return x / y
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
            elif highest <= 1 and (op == "*" or op == "/"):
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
            if input[start-2].isnumeric():
                char_l = "*"
                paren_converted = True

            percent_adjust = 0
            if end+1 < len(input):
                if input[end+1].isnumeric():
                    if not(paren_converted):
                        char_r = "*"
                    else:
                        raise ParenthesisError
                elif input[end+1] == "%":
                    ans = self.getPercent(f"{ans}%")
                    percent_adjust = 1

            # restructure input
            input = input[0:start-1] + char_l + str(ans) + char_r + input[end+1+percent_adjust:]

            paren_count -= 1

        # set the terms
        terms = re.split(r'[\/\*\-\+\^]', input)

        # set the operators
        operators = re.findall(r'[\/\*\-\+\^]', input)
        operators = list(filter(None, operators))

        # set the operator's highest precedence in the equation
        self.assessPrecedence(operators)

        while len(terms) > 1:
            # evaluate terms with highest operator precedence
            i = 0
            while i < len(operators):
                op = operators[i]

                if(self.precedence[op] == self.highest):

                    # simplify terms
                    x = self.getPercent(terms[i])
                    y = self.getPercent(terms[i+1])
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

        # evaluate percentage
        result = self.getPercent(terms[0])

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
        if self.interface == "app":
            m_input = MagicInput(self.e.get())
        elif self.interface == "cli":
            m_input = MagicInput(self.e)

        error = m_input.validate()

        if error == "":
            # initialize precedence for EMDAS
            self.precedence = {
                "^": 3,
                "/": 2,
                "*": 2,
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