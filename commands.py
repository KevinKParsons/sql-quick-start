# Instructions:
# To Run File in Console (Run Python Script Interactively to Enter Commands After It Runs):
#   PyCharm - Ctrl+Shift+A - search 'Run file in Python console' to run the currently selected file in console
#   so commands can be entered in context after its finished running the script. Afterwards can just hit run button
#   as usual to continue running in console.
#       Use 'main.printAll()' after running file in console to manually run commands.
# Make sure don't have multiple connection to the database by having multiple python consoles open at a time.
#
# Overview:
# Program uses SQLite serverless SQL file as database on local drive. SQLAlchemy is used as Python library for SQL
# and SQLAlchemy ORM is used to map database information to Python objects so that no SQL language needs to be used.
#
# Notes:
# If get different thread errors when using 'Run file in Python Console' interactive mode.
# May be best to run the script as shown here with new main object creation, sql commands, then close and repeat.
#
# Use SQLite DB Browser to manually add columns to tables or change database schema or create new tables to match models
# in this app. That way when SQLAlchemy connects by running this app it checks that the database schema matches models
# and doesnt throw an error (Confirmed this works). Can always delete the database and recreate it from programmatic approach from scratch
# as an alternative to this method.
#
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
#
# To persist our User object, we Session.add() it to our Session:
# 	>>> ed_user = User(name='ed', fullname='Ed Jones', nickname='nickname_eds')
# 	>>> session.add(ed_user)
# 	At this point, we say that the instance is pending; no SQL has yet been issued and the object is not yet represented by a row in the database. The Session will issue the SQL to persist Ed Jones as soon as is needed, using a process known as a flush


from models import MainClass, Employee, Department


# Initiate Connection
main = MainClass()
# main.resetAll()  # Reset database

# Print All
main.printAll()

# Add Employee
main.s.add(Employee(name='john'))
main.s.commit()

# Update Employee Name
first_employee = main.s.query(Employee)[0]
first_employee.name = 'George_4'
main.s.commit()
print(main.s.query(Employee)[0].name)

# Add Existing Employee to Department
department = main.s.query(Department)[0]
employee = main.s.query(Employee)[2]
employee.departments.append(department)  # Works
main.s.commit()
print(main.s.query(Employee)[0].departments)

# Update Employee Nick Name
print(main.s.query(Employee)[3].nickName)
main.s.query(Employee)[3].nickName = 'test'
main.s.commit()
print(main.s.query(Employee)[3].nickName)

# Print All
main.printAll()

# Close Connection
main.s.close()

