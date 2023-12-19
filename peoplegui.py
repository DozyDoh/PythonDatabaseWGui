"""
Implement a GUI for viewing and updating class instances stored in a shelve;
the shelve lives on the machine this script runs on, as 1 or more local files;
"""

###  IMPORTS   ####

#  An import * statement will import all the public names (functions, classes, variables) from a module into the current namespace.
from tkinter import *
from tkinter.messagebox import showerror
import shelve



### GLOBAL VARS ####

shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')



###   Functions    ####

def makeWidgets():
    
    # Here we're making the entries variable a global variable, this variable is a dictionary used to store user input from our text box widgets and making it global means that we can change its value outside of this function scope, which we need in our functions for fetchRecord and updateRecord.  We are also making the window variable global so that we can access it in our mainloop function.
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
        # In each call we are specifying the parent widget (form) and on one we are specifying the text for that objects label (text=label).  Simply the lab object is the label of our text box, and the ent object is the text box itself.
        lab = Label(form, text=label)
        ent = Entry(form)
        # the grid methods are used to place the widgets in the parent widget.  The grid method takes two arguments, row and column.  The row and column arguments specify the row and column in which the widget should be placed.  The rows and columns are numbered from zero, so the first row is row 0, the second row is row 1, and so on.  The first column is column 0, the second column is column 1, and so on.
        #  In this case the row is specified by the ix variable, which is the index we created with enumerate (we iterate from 0 to len(fieldnames)).
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        # The entries dictionary is a dictionary that maps the field names to the Entry widgets.  The key is the field name (label) and the value is the Entry widget text box (ent).
 
        entries[label] = ent
    #  Each of these buttons calls a function according to the command parameter.  The command parameter is a function object.  The function object is called when the button is clicked.  We are also specifying alignment information for the buttons.  Note that we are only calling a function for Fetch and Update, for Quit, we are calling window.quit which is builtin.
    Button(window, text="Fetch",  command=fetchRecord).pack(side=LEFT)
    Button(window, text="Update", command=updateRecord).pack(side=LEFT)
    Button(window, text="Quit",   command=window.quit).pack(side=RIGHT)
    return window

### Note in this case we have an entries dictionary that maps the field names of the Entry widgets which are the user input, and we have our db dictionary which is our database.  We are using the entries dictionary to get the user input and we are using the db dictionary to store the user input.

def fetchRecord():
    # The entries dictionary maps to user input.  The key is the field name and the value is the user input, in this case entries['key'] is the user input for the key field.  Note that the get method retrives the value of the key from the dictionary only once it is called.  So up until this point, we have not done anything with the user input from the code above, it is until this point that we are retrrieving something from the user input text.
    key = entries['key'].get()
    try:
        #  Here we check to see if the key is in the db dictionary (this dictionary is our shelve object which represents our persistance layer).  If it is we get the value of the key and assign it to record.  If it isn't we show an error message.
        record = db[key]                      
    except:
        showerror(title='Error', message='No such key!')

    #  Note that here we are calling else after try and not if, which means that if the try block executes without an exception, the else block will execute.  If there is an exception, the else block will not execute.
    else:
        # Here we are iterating over the fieldnames tuple and deleting the text (basically clearing our user inputs), if any exist, in the entries dictionary for each field (name, age, job, pay).  Then we are inserting the value of the field from the record object (the record object being the db shelve object in this case) into the entries dictionary for each field.  We are also specifically grabbing the entries[field] final value after assigning a record from the db to our record variable.
        for field in fieldnames:
            entries[field].delete(0, END)
            #  In this line, we are using the getattr function to get the value of field (name, age, job, pay) from the record object (record = db[key] or db[<Key Value>]).  The getattr function takes two arguments, the object and the attribute name.  This essentially extracs a value based on the record object (which is our shelve object) and the field name (name, age, job, pay).
            #  Note that repr() is a special method for representing objects in a class as a string.  It is similar to str() but it is used for debugging and development.  It is used here to convert the value of the field to a string.

            entries[field].insert(0, repr(getattr(record, field)))

            #  In short, we are getting the key value first from our user inputs, and then based on this key, we are fetching the appropriate record from the shelve object (the key must exist).  First deleting any text in the user input, and then inserting the value of the field from the record object (shelve object) thereby retrieving the values from the shelve object and displaying them in the user input text boxes.

def updateRecord():
    # Here we are getting the user input for the key field.
    key = entries['key'].get()
    #  Here we check to see if the key is in the db dictionary (or shelve object).  If it is, we get the record tied to the key in db and assign it to the record variable.  If it isn't, we create a new Person object and assign it to record.
    if key in db:
        #  Here db[key] is essentially a Person object, which we are referencing via the key.  Remember that a shelve object works like a persistent dictionary, it has a key and value pair.  In our case, the key is the key field and the value is a Person (or Manager ) object if it exists.  If it doesn't, we're skipping down to else: below and creating a new Person object and adding it to our database.
        record = db[key]                      # Use key to get record from db, if it exists, if not go to else below:
    else:
        #  Here we are importing the Person class from the person_alternative module.  This is the class that we used to create the record objects in the first place.  We are creating a new Person object and assigning it to the record variable.
        from person_alternative import Person

        # Here we are instantiating a Person object and assigning it to the record variable.  Note that the Person class only defines default arguments for the pay and job fields, so we must specify the name and age fields in our call here (in this case they are ? marks, which are temporary, as we'll be assigning the values stored in our user input (entries) to these attributes of the object in our for loop below).  If you think about it, this also means that each of our objects inside of our database is a Person or Manager object which we can reference by key.
        record = Person(name='?', age='?')
    
    #  field (name, age, job, pay).  Now that we've instantiated our Person object, we are looping through field in fieldnames (name, age, job, pay) and using setattr (see below) to change the values of record to user input values in entries.
    for field in fieldnames:

        #  Here, we are getting each value from entries via entries[field].get() and running eval on each value.  Eval is a builtin function that takes user input and turns it into a string, similar to str().  We are then setting the value of the field in the record object (individual shelve record) to the value of the field in the entries dictionary via the setattr function.  
        
        #The setattr function takes three arguments, the object, the attribute name, and the attribute value.  In this case, the object is the record object, the attribute name is the field name, and the attribute value is the value of the field from the entries dictionary.

        # Essentially what we are doing here is transfering our user input data from entries dict to our record object (shelve object).
        setattr(record, field, eval(entries[field].get()))
    #  Finally, here we make a new entry in the db shelve object with the key of [key] and a value of record, which could be a record we retrieved and changed, or could also be a brand new Person object depending on our if key in db check.  One thing I noticed:  if we don't have a key here, does the program crash?  I think what actually happens is that having a blank key value is in and of itself a key, so when you search based on a blank key, you will get whatever records where saved for that object.
    db[key] = record




###  Start of Script Logic ###

db = shelve.open(shelvename)

window = makeWidgets()

window.mainloop()
db.close() # back here after quit or window close, this means that mainloop exits when the user closes the window or the gui quits
