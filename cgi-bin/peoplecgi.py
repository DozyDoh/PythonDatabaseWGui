"""
Implement a web-based interface for viewing and updating class instances
stored in a shelve; the shelve lives on server (same machine if localhost)
"""
###  IMPORTS  ###
import cgi, html, shelve, sys, os                   # cgi.test() dumps inputs

###  GLOBAL VARS  ###
shelvename = 'class-shelve'                   # shelve filename in cwd
fieldnames = ('name', 'age', 'job', 'pay')    #  Tupel of values which shouldnt change, notice that key is not included here.  We will be creating our key html row manually, as well as any other instances where we need key.

###  HTML    ####

form = cgi.FieldStorage()
# parse form data.  Note the object created from the FieldStorage call acts like a dict in many ways, allowing you to use .keys for example to get all the vars that were sent to the program.  I printed this and the output was a dict like object

#  print(form.keys())
print('Content-type: text/html')              # hdr, note that print inserts a newline after each print statement

sys.path.insert(0, os.getcwd())               # sys.path refers to the list of directories Python searches for imported modules.  Here we are inserting the current working directory to the beginning of the list (there's also sys.path.append, which adds a directory to the end of the list of directories for searching), so that we can import person_alternative.py from the current working directory.  This is necessary because the current working directory is not in the list by default.  This is necessary because we are importing person_alternative.py which is in the current working directory.  If we were to run this script from the command line, we would not need to do this because the current working directory is in the list by default.

# Main HTML Template
#  Note that we have 2 newlines between Content-type: text/html and the begging of our html string, which give us the 2 blank lines between our header and our html code whcih is required.  The first newline is from the print statement and the second is from the invisible \n in our html string.  Note that Multi-line strings always include newline characters even when you don't specify them.  This is why we have 2 newlines between our header and our html code.
replyhtml = """
<html>
<title>People Input Form</title>
<body>
<h2> <i>{}</i></h2>
<form method=POST action="peoplecgi.py">
    <table>
    <tr><th>key<td><input type=text name=key value="%(key)s">
$ROWS$
    </table>
    <p>
    <input type=submit value="Fetch",  name=action>
    <input type=submit value="Update", name=action>
</form>
</body></html>
""".format(form)
#  Note that we can combine string formatting methods, initially Im using {} and .format(form) to print the FieldStorage object, and we're using the placeholder method for replacing our values in each row.
#  I've inserted this line <h2> <i>{}</i></h2> to print out the dictionary-like object we get from cgi.FieldStorage().  Interestingly the object looks like the following:  FieldStorage(None, None, [MiniFieldStorage('key', 'bob'), MiniFieldStorage('name', "'Dozy duoer'"), MiniFieldStorage('age', "'100'"), MiniFieldStorage('job', "'homeless'"), MiniFieldStorage('pay', '0'), MiniFieldStorage('action', 'Update')])   This is what we get back from user input, notice that it also includes the action from our html buttons.  This is why we need to check for action in our form object below.  Note that the first 2 None's are the fp and environ variables, which are not used in this case (note that cgi module is deprecated now and multipart is recommended for parsing form data)

#  Note that we are including the first element for our text user input boxes (in this case the key text box) under <tr><th>, the key value determines the label of our text box.  Input type=text and name=key are the same for all rows, however we have a var for value (value="%(key)s").  In this case we are creating a named variable placeholder, which is used to retrieve a value from a dictionary, with the key given here.  Note:  A literal % is coded as %%, which makes sense in our example, so to get a single % you need to code %%.  This leaves us with %(key)s

#  From Learning Python:  Dictionary-Based Formatting Expressions As a more advanced extension, string formatting also allows conversion targets on the left to refer to the keys in a dictionary coded on the right and fetch the corresponding values.  This allows us to use formatting as a sort of templating tool:

#  '%(qty)d more %(food)s' % {'qty': 1, 'food': 'spam'}


# Here we are saving a HTML template element for each of our fieldnames (in this case age, name, job, pay) that we are going to insert into our HTML, replacing $ROWS$.  Also, nitice that we've already created a template for our first row which is for our key user input.
#  <tr> denotes the beginning of a row in a table, <th> denotes the header of the row, <td> denotes the data of the row.  Here, our heading <th> is our %s placeholder (name, age, job, pay), our data <td> is an <input> element.  The <input> element is used to create several different form controls, the type parameter determines what type of input we're creating.  In this case, we are using the user input we already collected from our html, and filling in the values that we need to display.  The name parameter is used to identify the form control when the form is submitted.  The value parameter is used to specify the initial value of the control.  Note also that we are including the newline char, since we are inserting this into our htmlreply above.
rowhtml  = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'
#  We are first constructing the format of each of our rows with %s as a variable placeholder.  Notice that we have this crasy thing here:  value="%%(%s)s">\n'  This is a way to escape the % sign, which is a special character in python.  We are using %s as a variable placeholder, however we are escaping the % sign with another % sign, which is why we have %%(%s)s.  Also, notice that we are actually nesting two placeholders %(%s)s.  This is because we are using the string formatting technique using a dictionary.  The way it works is we are first converting the internal (%s) to one of our variables in the loop (name, age, job, pay) which gives us %(name)s for example.  This format of %(name)s is the format we use to get a value from a dictionary that we specify.  So in effect we are getting the value of (name) from our dictionary.  The dictionary to be used is specified below in our main code structure.
# Note that we have a rowhtml variable which has our template, and below we have a rowshtml = '' variable which we are going to use to store our rowshtml for each iteration of our loop.  We are then going to replace $ROWS$ in our replyhtml with rowshtml, which will give us our final html page with all of our rowshtml inserted into our replyhtml.
rowshtml = ''
# Next we are iterating over fieldnames and creating a line for each item (name, age, job, pay) using our HTML template and adding it to rowshtml
for fieldname in fieldnames:

    # This is where we replace our %s placeholders with each field in fieldnames.
    # In this case, we are creating a tuple that contains fieldname 3 times for each fieldname in our loop.  We then use this as assignment for our variable placeholders inside rowhtml and then append each iteration to rowshtml, which gives us a row of html elements, each with each fieldname in fieldnames.  Notice that we are enclosing the value element twice with %(key)s, this means we're replacing the internal key with our fieldname leaving the result as "%(name)s", which is a way to reference a dictionary key for our variable.
    #  WE ARE FIRST INSERTING THE FIELDNAMES FOR OUR ROWS IN THE %S PALCEHOLDERS, AND THEN DOWN BELOW WE ARE REPLACING OUR %(%s)s with the actual value from our fields dictionary which is returned from either of our update and fetch funcitons.  This happens on line 146.
    rowshtml += (rowhtml % ((fieldname,) * 3))
# Here we are replacing $ROWS$ in our replyhtml with rowshtml, which gives us our final html page with all of our rowshtml inserted into our replyhtml.
replyhtml = replyhtml.replace('$ROWS$', rowshtml)


###   FUNCTIONS    ###

# This function is used to htmlize our dictionary values, which means transforming and escaping our values in case there are html special chars in the value.  We are also using repr to get the string representation of our dictionary values.  This is necessary because we are using eval in our updateRecord function below, which requires a string representation of our dictionary values.  TLDR this function transforms our dictionary values into a string representation and escapes any special chars in the value.

#  First we have our htmlize function that accepts a dictionary as an argument.  We then create a new copy of our dictionary from our argument dictionary.  We then iterate over each field in our fieldnames tuple and assign the value of each field to our new dictionary.  We then return our new dictionary.
def htmlize(adict):
    new = adict.copy()
    for field in fieldnames:                       # values may have &, >, etc.
        value = new[field]                         # display as code: quoted
        new[field] = html.escape(repr(value))       # html-escape special chars
    return new

#  This function takes our db and form as arguments and returns a dictionary with our name value pairs in a dict called fields.
def fetchRecord(db, form):
    try:
        # Here we are getting the key value from our FieldStorage dictionary type object 
        #print(form['key'].value)
        key = form['key'].value
        # Next, we're using the key to query our shelve database and storing the record returned in the record variable.
        record = db[key]
        # Next, we are using the __dict__ attribute of our record object to get a dictionary of our record object attributes.  I think we need this since our record is a class object, we need to use __dict__ to get a dictionary of our attributes (Note that if the key does not exist, )
        fields = record.__dict__
        # Next, we are adding our key to our fields dictionary, which is the key we used to query our shelve database.
        fields['key'] = key                        # to fill reply string
    except:
        # dict.fromkeys() returns a dictionary jwith the specified keys and value.  In this case, we are creating a dictionary with our fieldnames as keys and ? as the value.  We are then assigning 'Missing or invalid key!' string to our fields['key'] key.
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing or invalid key!'
    #  In effect, this returns a record with a key of 'Missing or invalid key!' if the key does not exist in our shelve database, and also assigns ? to the rest of the record keys.  If the key does exist, we get a record with the key we queried and the rest of the keys are assigned the values from our shelve database.    
    return fields

def updateRecord(db, form):
    # Here we are checking for the existance of any 'key' in form (FieldStorage), if there is no 'key' in our FieldStorage user input, then we are assigning a dictionary with our fieldnames as keys and ? as the value to our fields variable.  We are then assigning 'Missing key input!' to our fields['key'] key (pretty much the same as above)
    if not 'key' in form:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing key input!'

    else:
        #  If we do have a key in our FieldStorage user input, we are assigning its value (form['key'].value) to our key variable.  
        key = form['key'].value
        # Next we check to see if our key is in the shelve obj db.
        if key in db:
            #  If it is, we assign the record to our record variable.
            record = db[key]                       # update existing record
        else:
            # If it is not, we create a new Person object and assign it to our record variable.
            from person_alternative import Person
            record = Person(name='?', age='?')
        #  Next we iterate over each field in our fieldnames tuple and assign the value of each field to our record object.
        for field in fieldnames:
            #  Remember, setattr takes 3 arguments:  Object to set attribute on, attribute name to change, and attribute value to set.  In this case, we are setting the attribute of our record object to the value of our form object.  Note that we are using eval to evaluate the value of our form object, which is necessary since our form object is a string representation of our dictionary values.  We are using eval to convert our string representation of our FieldStorage values to a dictionary.
            setattr(record, field, eval(form[field].value))
        # Next we are updating our shelve database with our new record object.
        db[key] = record
        # Next we are assigning our fields variable to a dictionary of our record object attributes.  I think we need this since our record is a class object, we need to use __dict__ to get a dictionary of our attributes
        fields = record.__dict__
        # Next we are adding our key to our fields dictionary, which is the key we used to query our shelve database (note: this is because our field from fieldnames does NOT include key)
        fields['key'] = key
    # Here we return our fields dictionary, which is a dictionary of our record object attributes.
    return fields


###   MAIN SCRIPT   ###
#  First thing we do is open shelve object and assign it to db variable.
db = shelve.open(shelvename)

#  Here we are assigning form['action'].value if 'action' exists in form to action variable, otherwise return None and assign to action var.
#  Here form['action'].value is fetching the value of element 'action' from our html peoplecgi.html which depends on the button clicked.  The Fetch button will have an 'action' of 'Fetch' and the Update button will have an 'action' of Update.

action = form['action'].value if 'action' in form else None

#  Here, if the value from our button is Fetch, we are calling fetchRecord func with (db, form) as arguments and assigning the returned dictionary to fields.  Otherwise, we are assigning a dictionary with our fieldnames as keys and ? as the value to our fields variable.  We are then assigning 'Missing or invalid action!' to our fields['key'] key (pretty much the same as above)
if action == 'Fetch':
    fields = fetchRecord(db, form)
# If the value from our button is Update, we are calling updateRecord func with (db, form) as arguments and assigning the returned dictionary to fields
elif action == 'Update':
    fields = updateRecord(db, form)
#  If the value from our button is neither Fetch or Update, we are assigning a dictionary with our fieldnames as keys and ? as the value to our fields variable.  We are then assigning 'Missing or invalid action!' to our fields['key'] key (pretty much the same as above)
else:
    fields = dict.fromkeys(fieldnames, '?')        # bad submit button value
    fields['key'] = 'Missing or invalid action!'
db.close()
#  In the final line, we're using our htmlize function to htmlize our fields dictionary and then inserting the values into our replyhtml template and printing it out to the browser.  THIS IS WHERE WE ASSIGN THE VALUE OF %(name)s, %(age)s, %(job)s, %(pay)s, %(key)s according to the fields dictionary after applying htmlize.
print(replyhtml %  htmlize(fields))

###  The plot thickens  ###
#  When looking at the output of running htmlize and giving it fields as a parameter, we get the output {'name': '&#x27;?&#x27;', 'age': '&#x27;?&#x27;', 'job': '&#x27;?&#x27;', 'pay': '&#x27;?&#x27;', 'key': 'Missing or invalid action!'}  Notice that we have &#x27; in each of our values.  This is because we are using html.escape(repr(value)) in our htmlize function.  html.escape() escapes the characters in a string using html entities.  html entities are used to display reserved characters in html.  In this case, &#x27; is the html entity for the single quote character.  This is why we are seeing &#x27; in our output.  repr() returns a string containing a printable representation of an object.  In this case, we are using repr() to get the string representation of our dictionary values.  This is necessary because we are using eval in our updateRecord function below, which requires a string representation of our dictionary values.  TLDR this function transforms our dictionary values into a string representation and escapes any special chars in the value.
# print(htmlize(fields))

#  For our string formatting, note that we are first replacing our %s placeholders with each field in fieldname.  For the value this gives us %(name)s for example.  This format of %(name)s is the format we use to get a value from a dictionary that we specify.  So in effect we are getting the value of (name) from our dictionary.  We do this at the final line of our code

