import numpy as np

class Matrix:
    def __init__(self, a,b,c,d):
        self.matrix  = np.array([[a,b],[c,d]])

    def __str__ (self):
        return (f"[{self.matrix[0][0]}, {self.matrix[0][1]};\n "
                f"{self.matrix[1][0]}, {self.matrix[1][1]}]")

    def __repr__(self):
        return (f"Matrix({self.matrix[0][0]},{self.matrix[0][1]},"
                f"{self.matrix[1][0]},{self.matrix[1][1]})")

    def __add__(self,other):
        temp = self.matrix + other.matrix
        return Matrix(temp[0][0],temp[0][1],temp[1][0],temp[1][1])

    def __mul__(self,other):
        temp = np.dot(self.matrix, other.matrix)
        return Matrix(temp[0][0],temp[0][1],temp[1][0],temp[1][1])
