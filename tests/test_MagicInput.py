import unittest
from src.MagicInput import MagicInput

class TestMagicInput(unittest.TestCase):
  def test_is_integer(self):
    # Test if is_integer returns correct value
    magic_input = MagicInput("2")
    self.assertTrue(magic_input.isInteger())