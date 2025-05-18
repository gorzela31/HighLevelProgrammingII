#ZADANIE 2.2 typing for function
from typing import List

def average(numbers: List[float]) -> float:
    return sum(numbers) / len(numbers)


#Testowanie
print("Average for list of floats: ", average([1.0, 2.0, 3.0, 4.0, 5.0]))
#Jak podamy inty to nie ma problemu:
print("Average for list of ints: ", average([1, 2, 3, 4, 5]))
#żeby był wymagany float to trzebaby zaimplementowac sprawdzenie w funkcji i ewentualne rzucenie wyjątku