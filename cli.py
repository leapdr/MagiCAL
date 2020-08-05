from MagicMath import *

start_message = """
Welcome to MagiCAL CLI
by Aaron Basco

Command List:
(0) - Evaluate expression
"""
print(start_message)

com = input("Select command from list to start: ")

if com == "0":
    expr = input("Enter expression to be evaluated: ")
    
    math = MagicMath("cli", expr)
    math.parse()