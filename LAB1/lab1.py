#ZADANIE 1
import model_ai
import matrix

object1 = model_ai.ModelAI("Name1",1.0)
object2 = model_ai.ModelAI("Name2",2.0)
object3 = model_ai.ModelAI("Name3",3.0)

print(object1.ile_modeli())

objectFromFile = model_ai.ModelAI.z_pliku("model.json")

print(object1.ile_modeli())
print(objectFromFile.modelName)

#ZADANIE 2

m1 = matrix.Matrix(1,2,3,4)
m2 = matrix.Matrix(1,2,3,4)
print(m1.matrix)
print(m2.matrix)
print(m1+m2)
