class Matrix:
    def __init__(self, a,b,c,d):
        self.matrix  = [[a,b],[c,d]]

    def __add__(self,other):
        temp = [[(self.matrix[0][0]+other.matrix[0][0]),(self.matrix[0][1]+other.matrix[0][1])],
                      [(self.matrix[1][0]+other.matrix[1][0]),(self.matrix[1][1]+ other.matrix[1][1])]]
        return temp
