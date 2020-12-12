class Error(Exception): 
  pass

class DecimalError(Error):
  pass
class OperatorError(Error):
  message = ""

  def __init__(self, error_type, error_message = ""):
    base_message = f"Operator Error: ({error_type})"
    if(error_type == 0):
      type_message = "Function and sign association"
    elif(error_type == 1):
      type_message = "Operator at the begging of expression"
    elif(error_type == 2):
      type_message = "Invalid operation"
    elif(error_type == 3):
      type_message = "Missing term"

    self.message = base_message + type_message + error_message

  def __str__(self):
    return self.message
  
class ParenthesisError(Error):
  def __init__(self, error_type, error_message = ""):
    base_message = f"Group Error ({error_type}): "
    if(error_type == 0):
      type_message = "Illegal end of term"
    if(error_type == 1):
      type_message = "Malformed groupings"
    if(error_type == 2):
      type_message = "Missing Term in group"
    if(error_type == 3):
      type_message = "Mismatch group sign"
    if(error_type == 4):
      type_message = "Unclosed or unopened group"
    if(error_type == 5):
      type_message = "Missing group operation"

    self.message = base_message + type_message + error_message

  def __str__(self):
    return self.message

class AbsoluteValueError(Error):
  pass
class ConstantError(Error):
  def __init__(self, error_type, error_message = ""):
    base_message = f"Constant Error ({error_type}): "
    if(error_type == 0):
      type_message = "Misplaced constant"

    self.message = base_message + type_message + error_message

  def __str__(self):
    return self.message

class PercentSignError(Error):
  pass

class FactorialSignError(Error):
  pass

class UnrecognizedFunction(Error):
  pass

class UnrecognizedCharacter(Error):
  pass

class InputError(Error):
  def __init__(self, error_type, error_message = ""):
    base_message = f"Input Error ({error_type}): "
    if(error_type == 0):
      type_message = "Integer required"
    if(error_type == 1):
      type_message = "Insuficient input for function"

    self.message = base_message + type_message + error_message

  def __str__(self):
    return self.message

class OutputError(Error):
  def __init__(self, error_type, error_message = ""):
    base_message = f"Output Error ({error_type}): "
    if(error_type == 0):
      type_message = "Undefined for values outside [-1, 1]"

    self.message = base_message + type_message + error_message

  def __str__(self):
    return self.message