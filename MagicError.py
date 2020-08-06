class Error(Exception): 
    pass 
class DecimalError(Error):
    pass
class OperatorError(Error):
    pass
class ParenthesisError(Error): 
    pass 
class PercentSignError(Error):
    pass

class UnrecognizedFunction(Error):
    pass

class UnrecognizedCharacter(Error):
    pass