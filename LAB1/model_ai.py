import json

class ModelAI:
    ModelCounter = 0

    def __init__(self,modelName, modelVersion):
        self.modelName = modelName
        self.modelVersion = modelVersion
        self.nowy_model()

    def nowy_model(self):
        ModelAI.ModelCounter += 1

    @classmethod
    def ile_modeli(cls):
        return (f"Liczba utworzonych modeli:"
                f"{cls.ModelCounter}")

    @classmethod
    def z_pliku(cls, filename):
        with open(filename, "r") as f:
            text = json.load(f)
        return cls(text["name"], text["version"])
