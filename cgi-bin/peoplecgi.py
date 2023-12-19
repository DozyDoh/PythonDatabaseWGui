"""
Implement a web-based interface for viewing and updating class instances
stored in a shelve; the shelve lives on server (same machine if localhost)
"""
###  IMPORTS  ###
import cgi, html, shelve, sys, os                   # cgi.test() dumps inputs

###  GLOBAL VARS  ###
shelvename = 'class-shelve'                   # shelve files are in cwd
fieldnames = ('name', 'age', 'job', 'pay')    #  Tupel of values which shouldnt change

###  HTML    ####
form = cgi.FieldStorage()                     # parse form data.  Note the FieldStorage object created from the FieldStorage call acts like a dict in many ways, allowing you to use .keys for example to get all the vars that were sent to the program
# print(form.keys())
print('Content-type: text/html')              # hdr, blank line is in replyhtml so we don't specify  a newline here
sys.path.insert(0, os.getcwd())               # so this and pickler find person

# main html template
replyhtml = """
<html>
<title>People Input Form</title>
<body>
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
"""
#  Note that we are including the first element for our text user input boxes (in this case the key text box) under <tr><th>, the key value determines the label of our text box.  Input type=text and name=key are the same for all rows, however we have a var for value (value="%(key)s").  In this case we are creating a named variable placeholder.  Note:  A literal % is coded as %%, which makes sense in our example, so to get a single % you need to code %%.  This leaves us with %(key)s

#  From Learning Python:  Dictionary-Based Formatting Expressions As a more advanced extension, string formatting also allows conversion targets on the left to refer to the keys in a dictionary coded on the right and fetch the corresponding values.  This allows us to use formatting as a sort of templating tool:

#  '%(qty)d more %(food)s' % {'qty': 1, 'food': 'spam'}

#  Here the (qty) and (food) in the formatstring refer to keys in the dictionary literal on the right and fetch the associated values.

# Here we are inserting HTML element for each input box besides key (in this case age, name, job, pay)
rowhtml  = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'  #  We are first constructing the format of each of our rows with %s as a variable placeholder
rowshtml = ''
# Next we are iterating over fieldnames and creating a line for each item (name, age, job, pay) and adding it to rowshtml
for fieldname in fieldnames:

    # Here we are inserting the currrent rowhtml format, however we are replacing the %s value in rowhtml, with fieldname for each instance
    # In this case, we are creating a tuple that contains fieldname 3 times for each fieldname in our loop.  We then use this as assignment for our variable placeholders inside rowhtml and then append each iteration to rowshtml, which gives us a row of html elements, each with each fieldname in fieldnames.  Notice that we are enclosing the value element twice with %(key)s, this means we're replacing the internal key with our fieldname leaving the result as "%(name)s", which is a way to reference a dictionary key for our variable.
    rowshtml += (rowhtml % ((fieldname,) * 3))
print(rowshtml)
replyhtml = replyhtml.replace('$ROWS$', rowshtml)


###   FUNCTIONS    ###
def htmlize(adict):
    new = adict.copy()
    for field in fieldnames:                       # values may have &, >, etc.
        value = new[field]                         # display as code: quoted
        new[field] = html.escape(repr(value))       # html-escape special chars
    return new

def fetchRecord(db, form):
    try:
        key = form['key'].value
        record = db[key]
        fields = record.__dict__                   # use attribute dict
        fields['key'] = key                        # to fill reply string
    except:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing or invalid key!'
    return fields

def updateRecord(db, form):
    if not 'key' in form:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing key input!'
    else:
        key = form['key'].value
        if key in db:
            record = db[key]                       # update existing record
        else:
            from person_alternative import Person              # make/store new one for key
            record = Person(name='?', age='?')     # eval: strings must be quoted
        for field in fieldnames:
            setattr(record, field, eval(form[field].value))
        db[key] = record
        fields = record.__dict__
        fields['key'] = key
    return fields


###   MAIN SCRIPT   ###
db = shelve.open(shelvename)
#  Here we are assigning form['action'].value if 'action' exists in form to action variable, otherwise return None and assign to action var.
#  Here form['action'].value is fetching the value of element 'action' from our html peoplecgi.html which depends on the button clicked.  The Fetch button will have an 'action' of 'Fetch' and the Update button will have an 'action' of Update.
action = form['action'].value if 'action' in form else None
#  If we get an action value of 'Fetch' we call fetchRecord, otherwise if its 'UPdate' we call updateRecord.
if action == 'Fetch':
    fields = fetchRecord(db, form)
elif action == 'Update':
    fields = updateRecord(db, form)
else:
    fields = dict.fromkeys(fieldnames, '?')        # bad submit button value
    fields['key'] = 'Missing or invalid action!'
db.close()
print(replyhtml % htmlize(fields))                 # fill reply from dict
