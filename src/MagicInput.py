
import re
import sys

from src.MagicError import *

# DEFINE CONSTANTS
TOSYMBOL = {
  "*": "×",
  "/": "÷"
}

LEFT  = ["√"]
RIGHT = ["!", "%"]

CONST = ["π", "ℯ"]
SIGNS = ["+", "-"]
OPS = ["*", "/", "+", "-", "m"]
FUNCS = ["abs", "asinh", "asin", "sinh", "sin", "acosh", "acos", "cosh", "cos", "atanh", "atan", "tanh", "tan", "ln", "log", "sqrt"]
OPEN_GROUP = ["(", "[", "|"]
CLOSE_GROUP = [")", "]", "|"]
GROUP_PAIR = {")": "(", "]": "[", "|": "|", "[": "]", "(": ")"}

class MagicInput(object):
  """The input object"""
  def __init__(self, input):
    """Object constructor"""

    # serialize input
    if type(input) != str:
      input = str(input)

    # replacement
    self.input = input.replace("÷", "/").replace("×", "*").replace("mod", "m").replace("√", "sqrt ")

  def isInteger(self):
    """Check if input is an number"""
    return self.input.isnumeric()

  def validate(self):
    """Validates the input"""
    input = self.input

    try:
      al = l = 0
      groups = dict.fromkeys(OPEN_GROUP, 0)

      # initialize flags
      is_opened = False
      is_abs_opened = False
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
      is_sqrt = False

      fn = p = ""
      f = 0

      # iterate through each character of expression to validate
      for i, c in enumerate(input):
        if p == "":
          p = c

          # assign
          is_op = p in OPS
          is_sign = p in SIGNS
          is_alpha = p.isalpha()
          is_sqrt = p == "√"

          if is_alpha:
            fn += p
          if p == "(":
            l += 1
            is_opened = True

          # parentheses
          if c in OPEN_GROUP:
            if c == "|":
              is_abs_opened = True

            groups[c] += 1


          # illegal start of expression
          if is_op and not is_sign:
            raise OperatorError(1)
          elif c == "%":
            raise PercentSignError
          elif c == "!":
            raise FactorialSignError
        else:
          if c == " ":
            if fn in FUNCS:
              fn = ""
            continue

          is_op = c in OPS
          is_sign = c in SIGNS
          is_dot = c == "."
          is_per = c == "%"
          is_alpha = c.isalpha()
          is_num = c.isnumeric()
          is_fac = c == "!"
          is_sqrt = c == "√"

          n = ""
          if i + 1 < len(input):
            n = input[i+1]

          # number
          if is_num:
            if p.isalpha() and fn != "" and fn not in FUNCS and fn not in OPS:
              raise UnrecognizedCharacter
            elif p == "%":
              raise PercentSignError
            elif p in CONST:
              raise ConstantError(0)
            fn = ""
            is_sign_used = is_op_used = False

          # constant
          elif c in CONST:
            if p == ".":
              raise DecimalError
            elif p in CLOSE_GROUP and not (p == "|" and groups["|"] == 1):
              raise ParenthesisError(0)
            elif p == "%":
              raise PercentSignError
            elif p == "!":
              raise FactorialSignError

          # function, alphabet
          elif is_alpha:
            fn += c

            if p == "%":
              raise PercentSignError
            elif p in CLOSE_GROUP and not (p == "|" and groups["|"] == 1):
              raise ParenthesisError(0)
            elif p == ".":
              raise DecimalError
            is_op_used = False

            if n == "":
              raise InputError(1)

          # decimal point / dot
          elif is_dot:
            if is_dot_used or p == ".":
              raise DecimalError

            if n == "" or (p in CONST and fn not in FUNCS):
              raise DecimalError
            
            is_dot_used = True
            is_op_used = False
            is_sign_used = is_op_used = False

          # percent
          elif is_per:
            alp = p.isalpha()
            if alp or p == "." or p in OPS or p == "":
              raise PercentSignError

          # factorial
          elif is_fac:
            pass

          # operators
          elif is_op:
            alp = p.isalpha()
            if p == ".":
              raise DecimalError
            elif alp and p not in OPS and is_sign_used:
              raise OperatorError(2)
            elif p in OPS:
              if c not in SIGNS or (p in SIGNS and is_sign_used):
                raise OperatorError(2)

            if not is_op_used:
              is_op_used = True
            elif c in SIGNS and not is_sign_used:
              is_sign_used = True

            if n == "":
              raise OperatorError(3)

            is_dot_used = False

          # groups
          if c in OPEN_GROUP and not (c == "|" and groups[c] == 1):
            if (c == "[" or (c == "|" and groups[c] == 0)) and (p.isnumeric() or p in CLOSE_GROUP):
              raise ParenthesisError(1)
            elif p == "%" or p == "!":
              raise ParenthesisError(5)

            is_dot_used = False
            is_sign_used = is_op_used = False

            groups[c] += 1
          elif c in CLOSE_GROUP and not(c == "|" and groups[c] != 1):
            if p in OPEN_GROUP and c == "|":
              raise ParenthesisError(2)
            elif p.isalpha():
              raise ParenthesisError(0)
            elif p == ".":
              raise DecimalError
            elif c != ")" and n != "" and n.isnumeric():
              raise ParenthesisError(5)
            elif p in CONST:
              raise ConstantError(0)

            groups[GROUP_PAIR[c]] -= 1

          if c in OPEN_GROUP and groups[c] < 0:
            raise ParenthesisError(3)

          p = c

      # End of for loop

      # mismatched left
      for c, v in groups.items():
        if v != 0:
          raise ParenthesisError(4)

      # illegal end of expression
      if is_op_used or is_sign_used:
        raise OperatorError(3)

      return ""
    except DecimalError:
      return "Decimal Error"
    except OperatorError as e:
      return str(e)
    except InputError as e:
      return str(e)
    except ConstantError as e:
      return str(e)
    except PercentSignError:
      return "Misplaced Percentage"
    except FactorialSignError:
      return "Misplaced Factorial"
    except UnrecognizedCharacter:
      return "Unrecognized Character in Expression"
    except UnrecognizedFunction:
      return "Unrecognized Function or Operation"
    except ParenthesisError as e:
      return str(e)
  
  @staticmethod
  def getTermsAndOps(expr):
    """(str) -> ((list, list))
    Collect all terms and operations from the expression
    >>> 1 + 32
    ([1, 32], ["+"])
    >>> 43 + 23 - 30
    ([43, 23, 30], ["+", "-"])
    """
    terms = []
    ops = []

    is_sign_used = False
    tmp_str = ""

    for x, c in enumerate(expr):
      if c in OPS:
        left = not(x != 0 and expr[x-1].isnumeric())
        right = expr[x+1] not in SIGNS

        if c in SIGNS and right and left:
          tmp_str = tmp_str + c
        else:
          ops.append(c)
          terms.append(tmp_str)

          tmp_str = ""
          is_sign_used = False
      else:
        tmp_str = tmp_str + c

    terms.append(tmp_str)

    # print(terms)
    # print(ops)

    return (terms, ops)

  @staticmethod
  def getTermsInTerm(expr):
    """(string) -> (list)
    Basically filters constants like pi from the expression
    
    >>> 2π
    ["2", "π"]
    """
    terms = []
    tmp_str = ""

    for x, c in enumerate(expr):
      if x!= 0 and c.isalpha() and (expr[x-1].isnumeric() or expr[x-1] in CONST):
        terms.append(tmp_str)
        tmp_str = c
      else:
        tmp_str = tmp_str + c
    terms.append(tmp_str)

    return terms
