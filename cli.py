#!/usr/bin/env python3

import sys

from src.MagicMath import *

# Execute arguments
if len(sys.argv) > 1:
  expr = sys.argv[1]
  
  math = MagicMath("cli", expr)
  math.parse()
  sys.exit()

# Enter CLI
intro_message = """
Welcome to MagiCAL CLI
by Aaron Basco
"""

# initialize command list for CLI
command_list = """
-------------------------
Command List:
(0) - Evaluate expression
(1) - Factorize integer
(2) - Use function
(-) - Quit CLI
-------------------------
"""

# initialize function list for CLI
function_list = """
Function List:
(0)  - [abs(x)] Absolute Value
(1)  - [acos(x)] Arc Cosine
(2)  - [acosh(x)] Inverse Hyperbolic Cosine
(3)  - [asin(x)] Arc Sine
(4)  - [asinh(x)] Inverse Hyperbolic Sine
(5)  - [atan(x)] Arc Tangent
(6)  - [atanh(x)] Inverse Hyperbolic Tangent
(7)  - [ceil(x)] Ceiling
(8)  - [conj(x))] Conjugate
(9)  - [cos(x)] Cosine
(10) - [cosh(x)] Hyperbolic Cosine
(11) - [cosh^-1(x)] Hyperbolic Arccosine
(12) - [cos^-1(x)] Inverse Cosine
(13) - [floor(x)] Flooring
(14) - [frac(x)] Fraction
(15) - [im(x)] Imaginary
(16) - [int(x)] Integer
(17) - [ln(x)] Natural Logarithm
(18) - [Log(x)] Logarithm
(19) - [ones(x)] One's Complement
(20) - [re(x)] Real
(21) - [round(x)] Round
(22) - [sgn(x)] Signum
(23) - [sin(x)] Sine
(24) - [sinh(x)] Hyperbolic Sine
(25) - [sinh^-1(x)] Hyperbolic Arcsine
(26) - [sin^-1(x)] Inverse Sine
(27) - [sqrt(x)] Square Root
(28) - [tan(x)] Tangent
(29) - [tanh(x)] Hyperbolic Tangent
(30) - [tanh^-1(x)] Hyperbolic Arctangent
(31) - [tan^-1(x)] Inverse Tangent
(32) - [twos(x)] Two's Complement
"""

# enable available functions
avail_func = {
  "9": ("cos", "c"),
  "10": ("cosh", "C"),
  "23": ("sin", "s"),
  "24": ("sinh", "S"),
  "28": ("tan", "t"),
  "29": ("tanh", "T"),
}

# display intro message
print(intro_message)

com = ""
while com != "-":
  # display list of available commands
  print(command_list)
  com = input("Select command from list to start: ")

  if com == "0":
    # for evaluation of expressions
    expr = input("Enter expression to be evaluated: ")
    
    math = MagicMath("cli", expr)
    math.parse()
  elif com == "1":
    # for factoring input
    expr = input("Enter an integer to be factorize: ")

    math = MagicMath("cli", expr)
    math.factorize()
  elif com == "2":
    # for calling a function
    print(function_list)
    f = input("Select function: ")

    if f in avail_func.keys():
      function = avail_func[f][1]
      expr = input("Enter x: ")

      math = MagicMath("cli", expr)
      result = FUNC_EVAL[function](float(expr))
      math.display(result)
    else:
      # unknown or unavailable function
      print("Sorry! The current function is unavailable, please wait for the next update")
    
  elif com == "-":
    # exit message
    print("Bye!")