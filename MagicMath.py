import sys
import re

class MagicMath(object):
    def __init__(self, input, end):
        self.e = input
        self.end = end

    def validate(self):
        input = self.e.get().replace("÷", "/")

        # TODO include validation for parenthesis
        pattern = re.compile(r'[0-9]+([\+\-\*\/\^][0-9]+)*')
        matches = pattern.finditer(input)
        
        try:
            if(input.count("(") != input.count(")")):
                ParenthesisError

            match = next(matches).group()
            return match == input or len(input) == 0
        except ParenthesisError:
            return "Malformed Expression"
        except StopIteration:
            return "Invalid Input"

    def solve(self, o, x, y):
        if(o == "^"):
            return x**y
        elif(o == "/"):
            try:
                result = x / y
                return result
            except ZeroDivisionError:
                print("Division by Zero")
                sys.exit()
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

    def evaluate(self, input):
        # evaluate parentheses
        paren_count = input.count('(')

        if(paren_count > 0):
            # get parenthesis clause
            pass

        # set the terms
        terms = re.split(r'[\/\*\-\+\^]', input)

        # filter out empty strings from list
        operators = re.split(r'\d+', input)
        # set the operators
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
                    res = self.solve(op, float(terms[i]), float(terms[i+1]))

                    # pop simplified terms and operator in the list
                    terms[i] = res
                    terms.pop(i+1)

                    operators.pop(i)

                    # reassess precedence
                    self.assessPrecedence(operators)

                    # break the loop to restart
                    break

                i += 1

        result = terms[0]
        return result

    def display(self):
        # format float with .0
        if self.answer % 1 == 0:
            self.answer = int(self.answer)

        self.e.delete(0, self.end)
        self.e.insert(0, str(self.answer))

    def parse(self):
        error = self.validate()

        if error == "":
            # initialize precedence for EMDAS
            self.precedence = {
                "^": 3,
                "/": 2,
                "*": 2,
                "+": 1,
                "-": 1
            }

            input = self.e.get().replace("÷", "/")
            self.answer = self.evaluate(input)
            
            # display answer
            self.display()

        else:
            self.e.delete(0, self.end)
            self.e.insert(0, error)