import unittest
from src.MagicInput import MagicInput

class TestMagicInput(unittest.TestCase):
  def test_is_integer(self):
    # Test if is_integer returns correct value
    magic_input = MagicInput("2")
    self.assertTrue(magic_input.isInteger())

  def test_validate_valid_expressions(self):
    # Test validate method for some valid expressions
    valid_expressions = [
      "3(4+2(7/3)*1)", # basic arithmetic
      "2cos sin tan (.3sin(.2))", # trigonometric
    ]

    for expr in valid_expressions:
      magic_input = MagicInput(expr)

      # validate returns empty string if expression is valid
      self.assertEqual(magic_input.validate(), "")

  def test_validate_invalid_expressions(self):
    # Test validate method for some invalid expressions
    invalid_expressions = [

    ]