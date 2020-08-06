class Error(Exception): 
    pass

class DecimalError(Error):
    pass
class OperatorError(Error):
    message = ""

    def __init__(self, error_type, error_message = "Operator Error: "):
        if(error_type == 0):
            type_message = "Function and sign association"
        elif(error_type == 1):
            type_message = "Operator at the begging of expression"
        elif(error_type == 2):
            type_message = "Invalid operation"
        elif(error_type == 3):
            type_message = "Missing term"

        self.message = error_message + type_message

    def __str__(self):
        return self.message
    
class ParenthesisError(Error): 
    pass 
class PercentSignError(Error):
    pass

class UnrecognizedFunction(Error):
    pass

class UnrecognizedCharacter(Error):
    pass