import sys

from tkinter import *
from tkinter import ttk as ttk

sys.path.insert(1, "./src")

from MagicMath import MagicMath

root = Tk()
root.title("MagiCAL")
root["bg"] = "#ECECEC"

style = ttk.Style()
style.configure("Fixed.TButton", font="TkFixedFont")

# style input
ttk.Style().configure('pad.TEntry', padding='7 7 7 7')

# create input
input = ttk.Entry(root, style='pad.TEntry', width=62)
input.grid(row=0, column=0, columnspan=8, padx=(5,0), pady=(5,0))

math = MagicMath("app", input, END)

# encode function
def encode(val):
    current = input.get()
    clear()
    input.insert(0, f"{current}{val}")

def factorizeInput():
    math.factorize()

# clear function
def clear():
    input.delete(0, END)

# eval function
def eval():
    math.parse()

# get button background image
button_bg = PhotoImage(file = r"res/btn_bg.png")

buttons = [i for i in range(10)] + [".", "%"] + [
    "÷", " mod ", "sin ", "cos ", "tan ",
    "×", "|x|", "sinh", "cosh ", "tanh ",
    "-", "C", "a×b", "π", "ℯ",
    "+", "=", "(", ")", "xⁿ"
]

row_fix = 2
for x, i in enumerate(buttons):
    # for numbers
    if str(i).isnumeric():
        # lambda i=i to create different functions
        buttons[i] = Button(root,
            bd=0, bg="#ECECEC",
            borderwidth=0,
            highlightthickness=0,
            compound=CENTER,
            padx=0, pady=0,
            text=i,
            image=button_bg,
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

        buttons[i].grid(row=row, column=col, padx=(5,0), pady=(5,0))
    # for symbols
    else:
        if i == "":
            pass
        else:
            if i == ".":
                row = 4
                col = 1
            elif i == "%":
                row = 4
                col = 2
            else:
                row = int((x-12)/5+1)
                col = (x-12)%5+3

            fn = ""
            encode_text = i
            if i == "=":
                fn = eval
            elif i == "C":
                fn = clear
            elif i == "a×b":
                fn = factorizeInput
            elif i == "xⁿ":
                encode_text = "^"

            buttons[x] = Button(root,
                bd=0, bg="#ECECEC",
                borderwidth=0,
                highlightthickness=0,
                compound=CENTER,
                padx=0, pady=0,
                text=i,
                image=button_bg,
                command=fn if fn else lambda x=x: encode(encode_text)
            )

            buttons[x].grid(row=row, column=col, padx=(5,0), pady=(5,0))

root.mainloop()
sys.exit()
