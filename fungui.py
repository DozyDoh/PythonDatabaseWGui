from tkinter import *
import random
fontsize = 30
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'cyan', 'purple']

def onSpam():
    # This Toplevel() function call is calling a window object
    popup = Toplevel()
    # Here we are using random to pick one of the colors at random and storing it in color
    color = random.choice(colors)
    # Label is a method from tkinter, it is a label.  In this case it is for our popup window, we are setting the parent as popup, the background as black, and the foreground or fg as color variable, which we picked at random.  Next we enclose and call .pack(fill=both) to align our object in the parent window, and fill both 
    Label(popup, text='Popup', bg='black', fg=color).pack(fill=BOTH)
    # This is strange... we are calling mainLabel.config inside the onSpam function, however we have defined this in line 29 which is executed at the global level and is not inside a function.  Does this mean that we are overriding the options from our global statement, with this line?  Test:  When we click onSpam, the popup window should only have the fg=color
    mainLabel.config(fg=color)

def onFlip():
    mainLabel.config(fg=random.choice(colors))
    main.after(250, onFlip)

def onGrow():
    global fontsize
    fontsize += 5
    mainLabel.config(font=('arial', fontsize, 'italic'))
    main.after(100, onGrow)

#  First we call Tk to create our main window
main = Tk()
# mainLabel stores the tkinter Label using main for the parent window, 'Fun Gui!' for text, and relief=RAISED which specifies the appearance of a decorative border around the label.
mainLabel = Label(main, text='Fun Gui!', relief=RAISED)
# Here we are specifying the font=font, fontsize, format, fg=color and bg=color esentially formatting our Label
mainLabel.config(font=('arial', fontsize, 'italic'), fg='cyan',bg='navy')
# Here we pack our mainLabel @ the top (side=TOP), expaded (expand=YES), and filled (fill=BOTH)
#  Note pack() organizes widgets in horizontal and vertical boxes that are limited to left, right, top, bottom positions offset and relative to each other within a frame.  For info on pack arguments, look here foo https://www.activestate.com/resources/quick-reads/how-to-use-pack-in-tkinter/
mainLabel.pack(side=TOP, expand=YES, fill=BOTH)
# Here we are creating buttons, which have functions attached to the command parameter.
Button(main, text='spam', command=onSpam).pack(fill=X)
Button(main, text='flip', command=onFlip).pack(fill=X)
Button(main, text='grow', command=onGrow).pack(fill=X)
main.mainloop()

