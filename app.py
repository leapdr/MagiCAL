from tkinter import *
from tkinter import ttk as ttk
from MagicMath import MagicMath

root = Tk()
root.title("MagiCAL")
root["bg"] = "#ECECEC"

style = ttk.Style()
style.configure("Fixed.TButton", font="TkFixedFont")

# style input
ttk.Style().configure('pad.TEntry', padding='7 7 7 7')

# create input
input = ttk.Entry(root, style='pad.TEntry', width=45)
input.grid(row=0, column=0, columnspan=6, padx=(5,0), pady=(5,0))

math = MagicMath("app", input, END)

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

# get button background image
button_bg = PhotoImage(file = r"res/btn_bg.png")

buttons = [i for i in range(10)]
row_fix = 2
for i in buttons:
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

    if(i == 0):
        row = 4
        col = 0
    else:
        # fix rows for (7 8 9)-first arrangement
        row = int((i-1)/3+1) 
        col = (i-1)%3

    buttons[i].grid(row=row, column=col, padx=(5,0), pady=(5,0))

# create dot button
button_dot = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text=".",
        image=button_bg,
        command=lambda: encode(".")).grid(row=4, column=1, padx=(5,0), pady=(5,0))

# create operation buttons
button_add = Button(root, 
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="+",
        image=button_bg,
        command=lambda: encode("+")).grid(row=4, column=3, padx=(5,0), pady=(5,0))

button_sub = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="-",
        image=button_bg,
        command=lambda: encode("-")).grid(row=3, column=3, padx=(5,0), pady=(5,0))

button_mul = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="×",
        image=button_bg,
        command=lambda: encode("×")).grid(row=2, column=3, padx=(5,0), pady=(5,0))

button_div = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="÷",
        image=button_bg,
        command=lambda: encode("÷")).grid(row=1, column=3, padx=(5,0), pady=(5,0))

button_equal = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="=",
        image=button_bg,command=eval).grid(row=4, column=4, padx=(5,0), pady=(5,0))

button_clear = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="C",
        image=button_bg,
        command=clear).grid(row=3, column=4, padx=(5,0), pady=(5,0))

button_open_paren = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="(",
        image=button_bg,
        command=lambda: encode("(")).grid(row=2, column=4, padx=(5,0), pady=(5,0))

button_close_paren = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text=")",
        image=button_bg,
        command=lambda: encode(")")).grid(row=2, column=5, padx=5, pady=(5,0))

button_mod = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="mod",
        image=button_bg,
        command=lambda: encode(" mod ")).grid(row=1, column=4, padx=(5,0), pady=(5,0))

button_percent = Button(root,
        bd=0, bg="#ECECEC",
        borderwidth=0,
        highlightthickness=0,
        compound=CENTER,
        padx=0, pady=0,
        text="%",
        image=button_bg,
        command=lambda: encode("%")).grid(row=4, column=2, padx=(5,0), pady=(5,0))

root.mainloop()