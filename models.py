from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class MainClass:
    # Create database file if not already created and connect to it
    def __init__(self):
        engine = create_engine('sqlite:///database.db')  # File name and relative dir
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)  # Create all tables in db if not already created
        self.s = session()

    # Print Database Info
    def printAll(self):
        print('\nDepartments: %i' % self.s.query(Department).count())
        for department in self.s.query(Department).all():
            print(department)
        print('\nEmployees: %i' % self.s.query(Employee).count())
        for employee in self.s.query(Employee).all():
            print(employee)
        print('')

    # Add Employees to Database (Helper Method - Takes arg of list of employee names as strings)
    def addEmployees(self, name_list):
        print('\nAdding Employees to Database')
        for employee in name_list:
            self.s.add(Employee(name=employee))
        self.s.commit()

    # Reset Database
    def resetAll(self):
        print('\nResetting Database')
        for department in self.s.query(Department).all():
            self.s.delete(department)
        for employee in self.s.query(Employee).all():
            self.s.delete(employee)
        self.s.commit()
        for department in ['IT', 'Finance']:
            self.s.add(Department(name=department))
        for employee in ['Kevin', 'John', 'Bill', 'Joe']:
            self.s.add(Employee(name=employee))
        self.s.commit()


# Department Table
class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship('Employee', secondary='department_employee_link')  # Many to Many

    def __repr__(self):
        return "<Department(id={}, name={}, employees={})>".format(self.id, self.name, len(self.employees))


# Employee Table
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nickName = Column(String)
    hired_on = Column(DateTime, default=func.now())
    departments = relationship('Department', secondary='department_employee_link')  # Many to Many

    def __repr__(self):
        return "<Employee(id={}, name={}, hired_on={}, departments={})>".format(self.id, self.name, self.hired_on,
                                                                                len(self.departments))


# Many to Many Association Table
class DepartmentEmployeeLink(Base):
    __tablename__ = 'department_employee_link'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
