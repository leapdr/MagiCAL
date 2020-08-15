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

class AbsoluteValueError(Error):
    pass

class PercentSignError(Error):
    pass

class UnrecognizedFunction(Error):
    pass

class UnrecognizedCharacter(Error):
    pass

class InputError(Error):
    def __init__(self, error_type, error_message = ""):
        base_message = "Input Error: "
        if(error_type == 0):
            type_message = "Integer required"
        if(error_type == 1):
            type_message = "Insuficient input for function"

        self.message = base_message + type_message + error_message

    def __str__(self):
        return self.message