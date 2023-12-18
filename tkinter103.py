from tkinter import *
from tkinter.messagebox import showinfo

def reply(name):
    showinfo(title='Reply', message='Hello %s!' % name)

top = Tk()
top.title('Echo')
top.iconbitmap('py-blue-trans-out.ico')

Label(top, text="Enter your name:").pack(side=TOP)
#  The Entry widget is a single-line text box.
ent = Entry(top)
#  The pack() method tells the widget to size itself to fit the given text.
ent.pack(side=TOP)
#  The lambda expression is a way to pass a function to a widget that requires a callback function.
#  A callback function is a function that is called when an event occurs, in this case when the user clicks the Submit button
#  ent.get is the callback function and it returns the text in the Entry widget.
btn = Button(top, text="Submit", command=(lambda: reply(ent.get())))
btn.pack(side=LEFT)

#  top.mainloop() is the main event loop. It waits for events to happen and processes them.
top.mainloop()