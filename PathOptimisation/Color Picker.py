import tkinter as tk
from tkinter import colorchooser

def choose_color():
    color = colorchooser.askcolor(title="Select Color")
    if color[1]:
        canvas.itemconfig(rect, fill=color[1])

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200, bg='white')
canvas.pack()

rect = canvas.create_rectangle(50, 50, 150, 150, fill='blue')

button = tk.Button(root, text="Choose Color", command=choose_color)
button.pack()

root.mainloop()