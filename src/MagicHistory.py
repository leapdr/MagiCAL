
def _historyCounter(func):
	def fn(self, *args, **kwargs):
		data = func(self, *args, **kwargs)

		self.currentSize = len(self.current)
		self.solutionsSize = len(self.solutions)

		return data
	return fn

class MagicHistory(object):
	currentHistoryLimit = 50
	solutionHistoryLimit = 50

	currentSize = 0
	solutionsSize = 0

	current = []
	solutions = []

	def __init__(self):
		pass

	# get From current
	@_historyCounter
	def getFromCurrent(self, index = 0):
		return self.current.pop(index)

	# add to current
	@_historyCounter
	def addToCurrent(self, entry):
		self.current.insert(0, entry)

	# get from solutions
	@_historyCounter
	def getFromSolutions(self, index = 0):
		return self.solutions.pop(index)

	# add solution to History
	# format (equation, answer)
	@_historyCounter
	def addSolution(self, entry):
		self.solutions.insert(0, entry)
