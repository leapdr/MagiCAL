import sys
import re

class MagicMath(object):
    def __init__(self, input, end):
        self.e = input
        self.end = end

    def validate(self):
        input = self.e.get()

        # TODO include validation for parenthesis
        pattern = re.compile(r'[0-9]+([\+\-\*\/\^][0-9]+)*')
        matches = pattern.finditer(input)
        
        try:
            match = next(matches).group()
            return match == input
        except StopIteration:
            return False

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

    def assessProcedence(self):
        operators = self.operators
        
        highest = 0
        for op in operators:
            if highest == 0 and (op == "+" or op == "-"):
                highest = 1
            elif highest <= 1 and (op == "*" or op == "/"):
                highest = 2
            elif highest <= 2 and (op == "^"):
                highest = 3
            elif highest <= 3 and (op == "(" or op == ")"):
                highest = 4

        self.highest = highest

    def evaluate(self):
        while len(self.terms) > 1:
            # get the operator with highest procedence
            i = 0
            while i < len(self.operators):
                op = self.operators[i]

                if(self.procedence[op] == self.highest):

                    # simplify terms
                    res = self.solve(op, float(self.terms[i]), float(self.terms[i+1]))

                    # pop simplified terms and operator in the list
                    self.terms[i] = res
                    self.terms.pop(i+1)

                    self.operators.pop(i)

                    # reassess procedence
                    self.assessProcedence()

                    # break the loop to restart
                    break

                i += 1

        result = self.terms[0]
        return result

    def display(self):
        # format float with .0
        if self.answer % 1 == 0:
            self.answer = int(self.answer)

        self.e.delete(0, self.end)
        self.e.insert(0, str(self.answer))

    def parse(self):
        if self.validate():
            # initialize procedence
            self.procedence = {
                "^": 3,
                "/": 2,
                "*": 2,
                "+": 1,
                "-": 1
            }

            input = self.e.get()

            # set the terms
            self.terms = re.split(r'[\/\*\-\+\^]', input)

            # filter out empty strings from list
            operators = re.split(r'\d+', input)
            # set the operators
            self.operators = list(filter(None, operators))

            # set the operator's highest procedence in the equation
            self.assessProcedence()

            self.answer = self.evaluate()
            
            # display answer
            self.display()

        else:
            self.e.delete(0, self.end)
            self.e.insert(0, "Invalid Input")