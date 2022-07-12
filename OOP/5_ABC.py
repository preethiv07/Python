from abc import ABCMeta, abstractmethod

class Shape(metaclass = ABCMeta): #No definition of its own
    #abstract class cannot instantiate an object
    @abstractmethod #decoartor
    def area(self): #area should be present in the derived classes
        return 0

class Square(Shape):
    side=3
    def area(self):
        return self.side * self.side

class Rectangle(Shape):
    width=5
    length=10
    def area(self):
        return self.width * self.length


sq=Square()
rect=Rectangle()
print("Area of the Square: ", sq.area())
print("Area of the Square: ", rect.area())
