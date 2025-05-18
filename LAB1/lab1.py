#ZADANIE 1
import model_ai
import matrix
print("Zadanie 1")
object1 = model_ai.ModelAI("Name1",1.0)
object2 = model_ai.ModelAI("Name2",2.0)
object3 = model_ai.ModelAI("Name3",3.0)
print(object1.ile_modeli())
objectFromFile = model_ai.ModelAI.z_pliku("LAB1/model.json")
print(object1.ile_modeli())
print(objectFromFile.modelName)

#ZADANIE 2
print("\nZadanie 2")
m1 = matrix.Matrix(1,2,3,4)
m2 = matrix.Matrix(2,0,1,2)
print("Macierz m1: \n", m1)
print("Macierz m2: \n", m2)
m3 = m1+m2
print("Przeciążenie operatora +:\n", m3)
m4 = m1 * m2
print("Przeciążenie operatora *:\n", m4)
print("Metoda specjalna __repr__ dla m1: \n", repr(m4))
