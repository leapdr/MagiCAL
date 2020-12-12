#!/usr/bin/env python3

import sys

import tkinter as tk
from tkinter import ttk as ttk

from src.MagicMath import MagicMath
from src.MagicHistory import MagicHistory

# initialize tk for UI
root = tk.Tk()
root.title("MagiCAL")
root["bg"] = "#ECECEC"

style = ttk.Style()
style.configure("Fixed.TButton", font="TkFixedFont")

# style input
ttk.Style().configure('pad.TEntry', padding='7 7 7 7')

# create input
input = ttk.Entry(root, style='pad.TEntry', width=62)
input.grid(row=0, column=0, columnspan=8, padx=(5,0), pady=(5,0))

# create the claculator with the tk input
math = MagicMath("app", input, tk.END)
history = MagicHistory()
history.addToCurrent("")

def encode(val):
  """Encode the given character to the input field"""
  current = input.get()
  clear()
  input.insert(0, f"{current}{val}")

  newCurrent = input.get()
  history.addToCurrent(newCurrent)

def factorizeInput():
  """Factorize the input and displays the multiplication"""
  math.factorize()

def clear():
  """Clears the input field"""
  input.delete(0, tk.END)

def undo():
  """Undo last action"""
  if(history.currentSize > 1):
    history.getFromCurrent()
    data = history.getFromCurrent()
    history.addToCurrent(data)

    clear()
    input.insert(0, f"{data}")

def eval():
  """Evaluates the given mathematical expression"""
  math.parse()

# get button background image
button_bg = tk.PhotoImage(file = r"res/btn_bg.png")
button_bg_2 = tk.PhotoImage(file = r"res/btn_bg_2.png")

# initialize buttons for the calculator
buttons = [i for i in range(10)] + [".", "%", "C", "="] + [
  "÷", " mod ", "sin ", "cos ", "tan ", "log",
  "×", "xⁿ", "sinh", "cosh ", "tanh ", "ln",
  "-", "|x|", "a×b", "π", "ℯ", "√",
  "+", "x!", "Re", "Im", "B", "B",
  "⎌", "i", "(", ")", "D", "D"
]

# display the defined buttons
row_fix = 2
for x, i in enumerate(buttons):
  btn_bg = button_bg

  # for numbers
  if str(i).isnumeric():
    # lambda i=i to create different functions
    btn = tk.Button(root,
      bd=0, bg="#ECECEC",
      borderwidth=0,
      highlightthickness=0,
      compound=tk.CENTER,
      padx=0, pady=0,
      text=i,
      image=btn_bg,
      command=lambda i=i: encode(i))

    if i == 0:
      row = 4
      col = 0
    else:
      # fix rows for (7 8 9)-first arrangement
      row = int((i-1)/3+1) 
      col = (i-1)%3

    if row == 1:
      row = 3
    elif row == 3:
      row = 1

    btn.grid(row=row, column=col, padx=(5,0), pady=(5,0))
  # for symbols
  else:
    # check span
    if i == "":
      pass
    else:
      cspan = 1

      # special button characters
      if i == ".":
        row = 4
        col = 1
      elif i == "%":
        row = 4
        col = 2
      elif i == "C":
        row = 5
        col = 0
      elif i == "=":
        row = 5
        col = 1
        cspan = 2
        btn_bg = button_bg_2
      else:
        row = int((x-14)/6+1)
        col = (x-14)%6+3
      
      # default padding
      pady = (5, 5 if row == 5 else 0)
      padx = (5, 5 if col == 8 else 0)

      # special buttons that do input operations
      fn = ""
      btn_txt = i
      if i == "=":
        fn = eval
      elif i == "C":
        fn = clear
      elif i == "⎌":
        fn = undo
      elif i == "a×b":
        fn = factorizeInput
      elif i == "xⁿ":
        i = "^"
      elif i == "x!":
        i = "!"

      # finally display the button using tk.Button
      btn = tk.Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=tk.CENTER,
        padx=0, pady=0,
        text=btn_txt,
        image=btn_bg,
        command=fn if fn else lambda i=i: encode(i)
      )

      btn.grid(row=row, column=col, padx=padx, pady=pady, columnspan=cspan)

root.mainloop()
sys.exit()
