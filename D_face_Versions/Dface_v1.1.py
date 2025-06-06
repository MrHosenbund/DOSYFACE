from tkinter import *


root  = Tk()

#create a label widgeht
first_label = Label(root, text="hello world")
second_label = Label(root, text=" test")


first_label.grid(row=0, column=0)
second_label.grid(row=8, column=4)

root.mainloop()
