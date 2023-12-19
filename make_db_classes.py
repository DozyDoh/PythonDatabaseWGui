import shelve
from person_alternative import Person
from person_alternative import Manager

#  This is what starts db with some records in it for bob, sue and tom.  We also save our database to a file called class-shelve which gives us persistence.  The shelve module is a built-in module that provides a dictionary-like object that is persistent.  The shelve module uses the pickle module to serialize objects so they can be saved to a file and restored later and is easier to code.

bob = Person('Bob Smith', 42, 30000, 'software')
sue = Person('Sue Jones', 45, 40000, 'hardware')
tom = Manager('Tom Doe',  50, 50000)

db = shelve.open('class-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()
