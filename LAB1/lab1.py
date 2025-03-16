import model_ai
import json

object1 = model_ai.ModelAI("Name1",1.0)
object2 = model_ai.ModelAI("Name2",2.0)
object3 = model_ai.ModelAI("Name3",3.0)

print(object1.ile_modeli())

objectFromFile = model_ai.ModelAI.z_pliku("model.json")

print(object1.ile_modeli())
print(objectFromFile.modelName)

# with open("model.json", "r") as f:
#     text = json.load(f)
#     print(text[0]["name"])
#     print(len(text))