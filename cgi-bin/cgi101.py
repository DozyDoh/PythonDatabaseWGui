#!/usr/bin/python
import cgi, html
form = cgi.FieldStorage()                  # parse form data
print('Content-type: text/html\n')        # hdr plus blank line
print('<title>Reply Page</title>') 
print('<h2> <i>%s</i></h2>' % form)       # html reply page
if not 'differentname' in form:

    print('<h1>Who are you?</h1>')
else:
    ###  For this part, I imported both cgi and html since .escape was not found for cgi.  Looks like cgi is being deprecated.
    print('<h1>Hello <i>%s</i>!</h1>' % html.escape(form['differentname'].value))

###  Notice here that we are printing html statements which are arranged into an html page and returned to the web browser from our previous page when a user clicks on submit.