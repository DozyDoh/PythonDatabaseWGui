from tkinter import *
from tkinter.messagebox import showinfo

class MyGui(Frame):
    def __init__(self, parent=None):
        """
        Initializes the class.
        
        Args:
            parent: The parent widget (optional).
        """
        Frame.__init__(self, parent)
        button = Button(self, text='press', command=self.reply)
        button.pack()  # Packs the button widget into the parent widget.
    def reply(self):
        showinfo(title='popup', message='Button pressed!')

if __name__ == '__main__':
    window = MyGui()
    window.pack()
    window.mainloop()

