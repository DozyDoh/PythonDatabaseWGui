from tkinter import *
from tkinter.messagebox import showinfo

def reply():
    showinfo(title='popup', message='Button pressed!')

window = Tk()
# Notice here that for the button we are specifying the window variable first, which is the Tk() function call, the text is the label of the button, and the command is the code that gets triggered:  In this case its the reply function
button = Button(window, text='press', command=reply)
button.pack()
window.mainloop()

