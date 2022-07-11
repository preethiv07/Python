class Employee:
    # Define an attribute called name
    name = "Ben"
    designation ="Engineer"
    sales =6

    def changeName (self):
        # Change the value of the attribute within a method
        if self.sales >=1:
            return "Target achieved"
        else:
            return "Target NOT achieved"

employee=Employee()
print(f' write something {employee.changeName()} |')
