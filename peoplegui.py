"""
Implement a GUI for viewing and updating class instances stored in a shelve;
the shelve lives on the machine this script runs on, as 1 or more local files;
"""
#  An import * statement will import all the public names (functions, classes, variables) from a module into the current namespace.
from tkinter import *
from tkinter.messagebox import showerror
import shelve
shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

def makeWidgets():
    # Here we're making the entries variable a global variable so that it can be accessed by the fetchRecord and updateRecord functions.
    global entries
    window = Tk()
    window.title('People Shelve')
    #  Frame is a container widget. It is used to group other widgets together in the GUI.
    form = Frame(window)
    form.pack()
    entries = {}
#  Enumerate is a built-in function that returns an enumerate object. It takes a sequence as an argument and returns a sequence of tuples. The first item in each tuple is an integer index and the second item is the item from the original sequence.

#     In this instance of enumerate, we're concatenating the tuple key to the tuple fieldnames, which is a variable that is storing a tuple of strings ('name', 'age', 'job', 'pay') This gives us ('key', 'name', 'age', 'job', 'pay') and we're iterating over that and enumerating each item in order.  So we get (0, 'key'), (1, 'name'), (2, 'age'), (3, 'job'), (4, 'pay') and we're unpacking each tuple into ix and label.
    
#Note that ('key',) is actually a string inside a tuple that we're adding to fieldnames which is also a tuple.
    
    for (ix, label) in enumerate(('key',) + fieldnames):
        #Note here that Label and Entry are both classes that are defined inside the tkinter module.  We don't need to specify the module name because we imported with *.  Look inside tkinter module to confirm Confirmed!!
        # In each call we are specifying the parent widget and on one we are specifying the text for that objects label.
        lab = Label(form, text=label)
        ent = Entry(form)
        # the grid methods are used to place the widgets in the parent widget.  The grid method takes two arguments, row and column.  The row and column arguments specify the row and column in which the widget should be placed.  The rows and columns are numbered from zero, so the first row is row 0, the second row is row 1, and so on.  The first column is column 0, the second column is column 1, and so on.
        #  In this case the row is specified by the ix variable, which is the index we create with enumerate.
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        # The entries dictionary is a dictionary that maps the field names to the Entry widgets.  The key is the field name and the value is the Entry widget text box.
        #  For example, in the first iteration, we are adding the key 'key' and the value ent to the entries dictionary.  In the second iteration, we are adding the key 'name' and the value ent to the entries dictionary.  And so on in effect making a new dictionary out of our initial key/value pair from enumerate.
        entries[label] = ent
    #  Each of these buttons calls a function according to the command parameter.  The command parameter is a function object.  The function object is called when the button is clicked.  We are also specifying alignment information for the buttons.
    Button(window, text="Fetch",  command=fetchRecord).pack(side=LEFT)
    Button(window, text="Update", command=updateRecord).pack(side=LEFT)
    Button(window, text="Quit",   command=window.quit).pack(side=RIGHT)
    return window

def fetchRecord():
    # This function gets the value of the literal 'key' in the entries dictionary.  If we have a record with that key in the db dictionary, we assign the value of that record to the record variable.  If we don't have a record with that key, we show an error message.
    key = entries['key'].get()
    try:
        #  Here we check to see if the key is in the db dictionary (this dictionary is our shelve object which represents our persistance layer).  If it is we get the value of the key and assign it to record.  If it isn't we show an error message.
        record = db[key]                      # fetch by key, show in GUI
    except:
        showerror(title='Error', message='No such key!')
    else:
        # In this loop, we are iterating over the fieldnames tuple.  For each fieldname using field, we are deleting any entry with that name first, and then inserting the key value pair from the record dictionary into the entry widget.
        for field in fieldnames:
            
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))

def updateRecord():
    key = entries['key'].get()
    if key in db:
        record = db[key]                      # update existing record
    else:
        from person_alternative import Person             # make/store new one for key
        record = Person(name='?', age='?')    # eval: strings must be quoted
    for field in fieldnames:
        setattr(record, field, eval(entries[field].get()))
    db[key] = record

db = shelve.open(shelvename)
window = makeWidgets()

window.mainloop()
db.close() # back here after quit or window close, this means that mainloop exits when the user closes the window or the gui quits
