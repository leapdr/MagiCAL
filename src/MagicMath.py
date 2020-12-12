import sys
import re

from math import *

from src.MagicError import *
from src.MagicInput import *

PI = pi
E = e

CONST_VAL = {
	"π": PI,
	"ℯ": E
}

DEG = lambda x: degrees(x)
RAD = lambda x: radians(x)

ANGLE_DEFAULT = RAD

FUNC_EVAL = {
	"abs": lambda x: abs(x),
	"acos": lambda x: DEG(acos(x)),
	"acosh": lambda x: acosh(x),
	"asin": lambda x: DEG(asin(x)),
	"asinh": lambda x: asinh(x),
	"atan": lambda x: DEG(atan(x)),
	"atanh": lambda x: atanh(x),
	"cos": lambda x: cos(ANGLE_DEFAULT(x)),
	"cosh": lambda x: cosh(ANGLE_DEFAULT(x)),
	"sin": lambda x: sin(ANGLE_DEFAULT(x)),
	"sinh": lambda x: sinh(ANGLE_DEFAULT(x)),
	"tan": lambda x: tan(ANGLE_DEFAULT(x)),
	"tanh": lambda x: tanh(ANGLE_DEFAULT(x)),
	"sqrt": lambda x: sqrt(x),
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
				self.display(0)
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

	def getFactorial(self, x):
		result = 1
		while x > 0:
			result *= x
			x -= 1

		return result

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
		match = ""
		is_abs_opened = False

		while i < len(input) and not end_found:
			if input[i] in OPEN_GROUP and match == "":
				match = input[i]
				is_abs = match == "|"
			
			if match != "": 
				if input[i] == match and not(is_abs_opened):
					if not(start_found):
						start = i
						start_found = True
					else:
						start_extra += 1

					if match == "|":
						is_abs_opened = True
						i += 1
						continue

				if input[i] == GROUP_PAIR[match]:
					if start_extra > 0:
						start_extra -= 1
					else:
						if not(end_found):
							end = i
							end_found = True

			i += 1

		return (start, end, is_abs_opened)

	def evaluateTerm(self, term, is_abs = False):
		term = str(term)

		try:
			# no need term evaluation
			result = float(term)
			return result if not is_abs else abs(result)
		except ValueError:
			# has to be evaluated

			interms = MagicInput.getTermsInTerm(term)
			if len(interms) > 1:
				result = 1
				for interm in interms:
					result *= self.evaluateTerm(interm)
				return result
			else:
				term = interms[0]

				# is term constant
				if term in CONST:
					return CONST_VAL[term]

				# get decimal value
				p = re.compile(r"([\+\-]?\d*(\.\d+)?)")
				d = list(filter(None, [m.group() for m in p.finditer(term)])).pop()
				i = term.index(d)

				pfn = re.compile(r"|".join(FUNCS))
				fns = list(filter(None, [m.group() for m in pfn.finditer(term)]))
				result = float(d)

				# right factorial
				j = len(d)+i
				while j < len(term):
					if term[j] == "!":
						result = self.getFactorial(result)
					j+=1

				# left
				i = len(fns)-1
				while i >= 0:
					if fns[i] in ["acos", "asin"] and (result < -1 or result > 1):
						raise OutputError(0)
					
					result = FUNC_EVAL[fns[i]](result)
					i -= 1

				# right percentage
				j = len(d)+i
				while j < len(term):
					if term[j] == "%":
						result /= 100
					j+=1

				return result if not is_abs else abs(result)

	def evaluate(self, input, is_abs = False):
		# evaluate group
		group_count = sum([input.count(i) if i != "|" else input.count(i) / 2 for i in OPEN_GROUP])
		while group_count > 0:
			indices = self.getIndicesMatchingParen(input)
			start = indices[0] + 1
			end = indices[1]
			is_expr_abs = indices[2]

			exp = input[start:end]

			group_count -= sum([exp.count(i) if i != "|" else exp.count(i) / 2 for i in OPEN_GROUP])
			ans = self.evaluate(exp, is_expr_abs)

			# replace grouping characters
			group_converted = False
			char_l, char_r = "", ""
			less_func = 0

			if start > 1:
				left = input[start-2]

				if left.isnumeric():
					char_l = "*"
					group_converted = True
				elif left in FUNCS:
					ans = self.evaluateTerm(f"{left}{ans}")
					group_converted = True
					less_func += 1

			percent_adjust = 0
			if end+1 < len(input):
				if input[end+1].isnumeric():
					if not(group_converted):
						char_r = "*"
					else:
						raise ParenthesisError(5)

			# round
			if input[start-1] == "[":
				ans = round(float(ans))

			# restructure input
			input = input[0:start-1-less_func] + char_l + str(ans) + char_r + input[end+1+percent_adjust:]

			group_count -= 1

		# set the terms and operators
		parts = MagicInput.getTermsAndOps(input)
		terms, operators = parts[0], parts[1]

		# set the operator's highest precedence in the equation
		self.assessPrecedence(operators)

		while len(terms) > 1:
			# evaluate terms with highest operator precedence
			for i, op in enumerate(operators):
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

		# evaluate term
		result = self.evaluateTerm(terms[0], is_abs)

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
			except ParenthesisError as e:
				self.display(e)
			except ZeroDivisionError:
				self.display("Division by Zero")
			except OutputError as e:
				self.display(e)

		else:
			self.display(f"{m_input.input}: {error}")