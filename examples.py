import databaseSecretSanta
from databaseSecretSanta import Employee, Department
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import sessionmaker
from secretSanta import main


# -------- Examples -------- #

# Add Employee
main.s.add(Employee(name='john'))
main.s.commit()

# Add Department
main.s.add(Department(name='IT'))
main.s.commit()

# Update Employee Name
first_employee = main.s.query(Employee)[0]
first_employee.name = 'New Name'
main.s.commit()


# Add New Employee to Department
new_department = Department(name='IT35')
new_employee = Employee(name='john35')
new_department.employees.append(new_employee)
main.s.add(new_department)
main.s.add(new_employee)
main.s.commit()

# Add Existing Employee to Department
first_department = main.s.query(Department).first()
first_employee = main.s.query(Employee)[0]
# first_department.employees.append(first_employee)  # Doesn't Work
first_employee.departments.append(first_department)  # Works
main.s.commit()

# Queries
main.s.query(Employee).all()
main.s.query(Employee).first()
main.s.query(Employee).first().departments  # Get Employee by ID
main.s.query(Employee).filter(Employee.id ==7).one().name  # Get Employee by ID
main.s.query(Department).filter(Department.id ==3).one().employees  # Get Department by ID
main.s.query(Employee).filter(Employee.name.startswith("C")).one().name
main.s.query(Employee).join(Employee.department).filter(Employee.name.startswith('C'), Department.name == 'Financial').all()[0].name
main.s.query(Employee).filter(Employee.hired_on < func.now()).count()
main.s.query(Department).filter(Department.employees.any(Employee.name == 'John')).all()[0].name

# Deletes
d = main.s.query(Employee).first()
main.s.delete(d)
main.s.commit()

# Delete All
for employee in main.s.query(Employee).all():
    main.s.delete(employee)
main.s.commit()

# If getting the following error:
# sqlalchemy.exc.ProgrammingError: (sqlite3.ProgrammingError) SQLite objects created in a thread can only be used in that same thread.
# Recreate the main object in the current thread by using the following commands.
# main = MainClass()
# main.printAll()

# Use session roll back to clear errors or close the connection:
# main.s.rollback()
# main.s.close()

# If getting the following error:
# “This Session’s transaction has been rolled back due to a previous exception during flush.”
# https://docs.sqlalchemy.org/en/13/faq/sessions.html#faq-session-rollback
# This is an error that occurs when a Session.flush() raises an exception, rolls back the transaction,
# but further commands upon the Session are called without an explicit call to Session.rollback() or Session.close().
