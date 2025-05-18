#ZADANIE 2.3 typing for Library class
from typing import Dict, Optional

class Library:
    def __init__(self, dictionary: Dict[str, str]):
        self.dictionary = dictionary
    
    def find_book(self, title: str) -> Optional[str]:
        if title in self.dictionary:
            return self.dictionary[title]
        else:
            return None

myLibrary = Library({
    "Harry Potter": "J.K. Rowling",
    "The Hobbit": "J.R.R. Tolkien",
    "1984": "George Orwell"
})
print(myLibrary.find_book("Harryi Potter"))  # Output: J.K. Rowling