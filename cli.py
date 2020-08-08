from MagicMath import *

intro_message = """
Welcome to MagiCAL CLI
by Aaron Basco
"""

command_list = """
-------------------------
Command List:
(0) - Evaluate expression
(1) - Factorize integer
(2) - Use function
(-) - Quit CLI
-------------------------
"""

print(intro_message)

com = ""
while com != "-":
    print(command_list)
    com = input("Select command from list to start: ")

    if com == "0":
        expr = input("Enter expression to be evaluated: ")
        
        math = MagicMath("cli", expr)
        math.parse()
    elif com == "1":
        expr = input("Enter an integer to be factorize: ")

        math = MagicMath("cli", expr)
        math.factorize()
    elif com == "-":
        print("Bye!")