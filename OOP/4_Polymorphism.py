# class Employee:
#         def setworkinghours(self):
#             self.workhours=40
#             return self.workhours
#
# class Trainee(Employee):
#     def setworkinghours(self):
#         self.workhours = 45
#         return self.workhours
#     def resethours(self):
#         super().setworkinghours() #To access parent class
#
# preethi=Employee()
# print("Employee: ",preethi.setworkinghours())
# conductor=Trainee()
# print("Trainee: ",conductor.setworkinghours())
# resetcond=Trainee()
# print("super: ",resetcond.setworkinghours())

#######################################
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width

# Here we declare that the Square class inherits from the Rectangle class
class Square(Rectangle):
    def __init__(self, length):
        super().__init__(length, length)

sq=Square(3)
print("Overriding: ",sq.area())

#############
# OPERATOR OVERLOADING
#############
class shape:
    def __init__(self, side):
        self.side=side

    def __add__(shape1,shape2): #Note Operator overloading doesnt use  self
        return 4*shape1.side+10*shape2.side

sq1=shape(3)
sq2=shape(3)
print("Sum of square of both sqaures= ",sq1 + sq2) #Throws errors without operator overloading because funtion present to add two shape classes
# print("dunder methods",dir())

