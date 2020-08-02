from tkinter import *
from tkinter import ttk as ttk
from MagicMath import MagicMath

# default button padding
BPAD = (15, 15)

root = Tk()
root.title("MagiCAL")

style = ttk.Style()
style.configure("Fixed.TButton", font="TkFixedFont")

# create input
input = Entry(root)
input.grid(row=0, column=0, columnspan=4)

math = MagicMath(input, END)

# encode function
def encode(val):
    current = input.get()
    clear()
    input.insert(0, f"{current}{val}")

# clear function
def clear():
    input.delete(0, END)

# eval function
def eval():
    math.parse()

buttons = [i for i in range(10)]
row_fix = 2
for i in buttons:
    # lambda i=i to create different functions
    buttons[i] = Button(root, padx=BPAD[0], pady=BPAD[1], text=i, command=lambda i=i: encode(i))

    if(i == 0):
        row = 4
        col = 0
    else:
        # fix rows for (7 8 9)-first arrangement
        row = int((i-1)/3+1) 
        col = (i-1)%3

    buttons[i].grid(row=row, column=col)

# create dot button
button_dot = Button(root, padx=BPAD[0], pady=BPAD[1], text=".").grid(row=4, column=1)

# create operation buttons
button_add = Button(root, padx=BPAD[0], pady=BPAD[1], text="+", command=lambda: encode("+")).grid(row=4, column=3)
button_sub = Button(root, padx=BPAD[0], pady=BPAD[1], text="-", command=lambda: encode("-")).grid(row=3, column=3)
button_mul = Button(root, padx=BPAD[0], pady=BPAD[1], text="*", command=lambda: encode("*")).grid(row=2, column=3)
button_div = Button(root, padx=BPAD[0], pady=BPAD[1], text="/", command=lambda: encode("/")).grid(row=1, column=3)
button_equal = Button(root, padx=BPAD[0], pady=BPAD[1], text="=", command=eval).grid(row=4, column=2)

button_clear = Button(root, padx=BPAD[0], pady=BPAD[1], text="CLEAR", command=clear).grid(row=5, column=0, columnspan=4)

root.mainloop()