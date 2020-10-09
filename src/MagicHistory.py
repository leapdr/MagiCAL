
class MagicHistory(object):
    currentHistoryLimit = 50
    solutionHistoryLimit = 50

    currentSize = 0
    solutionsSize = 0

    current = []
    solutions = []

    def __init__(self):
        pass

    def _historyCounter(func):
        def fn(self):
            func(self)
            self.currentSize = len(self.current)
            self.solutionsSize = len(self.solutions)
        return fn

    # get From current
    @_historyCounter
    def getFromCurrent(self, index = 0):
        return self.current.pop(index)

    # add to current
    @_historyCounter
    def addToCurrent(self, entry):
        self.current.insert(0, entry)

    # add solution to History
    def addSolution(self, entry):
        
        pass
