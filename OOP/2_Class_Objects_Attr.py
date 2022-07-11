# Class Attribute (All instance of the class is Impacted)
class Employee:
# This attribute is common across all instances of this
    numberOfEmployees = 0

employeeOne = Employee()
employeeTwo = Employee()
Employee.numberOfEmployees += 1
print("employee#1 instance" ,employeeOne.numberOfEmployees)
print("employee#2 instance",employeeTwo.numberOfEmployees)

#Instance Attributes(accessed only by objects/Instance
class EmployeeInt:
    def employeeDetails(self, name):
    # name is the instance attribute
        self.name = name
        return self.name

employeeOneInt = EmployeeInt()
employeeTwoInt = EmployeeInt()
print("#######INSTANCE ATTRIBUTE########")
print("employee#1 instance Attribute" ,employeeOneInt.employeeDetails('Ben'))
print("employee#2 instance Attribute",employeeTwoInt.employeeDetails('Men'))

#Static Method
class EmployeeStatic:
    def __init__(self, name):
        self.name = name

    @staticmethod #Decorator
    def employeeDetailStatic():
        print('welcome to static') # This cannot pass self.objectst (We can store information inside class variables and use it

employeeStatic = EmployeeStatic("rUBY")
print("#######STATIC METHOD########")
employeeStatic.employeeDetailStatic()





