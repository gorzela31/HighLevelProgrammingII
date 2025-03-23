# ZADANIE 1 - TEXT ANALYZER
class TextAnalyzer:
    def word_count(self, text):
        return len(text.split())
    
    def char_count(self, text):
        text = text.replace(" ", "")
        text = text.replace(",", "")
        text = text.replace(".", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        return len(text)
    
    def unique_words(self, text):
        return len(set(text.split()))
    
class AdvancedTextAnalyzer(TextAnalyzer):
    def __init__(self):
        self.positive_words = {"wspaniały", "cudowany", "niesamowity", "fantastyczny"}
        self.negative_words = {"okropny", "beznadziejny", "fatalny", "nędzny"}

    def sentiment_analysis(self, text):
        words = set(text.lower().split())

        if words & self.positive_words:
            return "Pozytywny"
        elif words & self.negative_words:
            return "Negatywny"
        else:
            return "Neutralny"


# #Zadanie 1
# text = "To był naprawdę wspaniały dzień!"
# text2 = "To był naprawdę Okropny dzień!"
# extendedAnalyzer = AdvancedTextAnalyzer()
# print("Word count: ", extendedAnalyzer.word_count(text))
# print("Char count: ", extendedAnalyzer.char_count(text))
# print("Unique words: ", extendedAnalyzer.unique_words(text))
# print("Sentiment: ", extendedAnalyzer.sentiment_analysis(text))
# print("Word count: ", extendedAnalyzer.word_count(text2))
# print("Char count: ", extendedAnalyzer.char_count(text2))
# print("Unique words: ", extendedAnalyzer.unique_words(text2))
# print("Sentiment: ", extendedAnalyzer.sentiment_analysis(text2))

#ZADANIE 2  - Inteligentny telefon

class Telefon:
    def __init__(self, model, producent):
        self.model = model
        self.producent = producent
    
class Komunikacja:

    def wyslij_wiadomosc(self, odbiorca, tresc):
        print("Wysyłanie wiadomości do: ", odbiorca)
        print("Treść: ", tresc)
    
class Rorzywka:
    def odtworz_muzyke(self, utwor):
        print("Odtwarzanie muzyki: ", utwor)

class Smartfon(Telefon, Komunikacja, Rorzywka):
    def __init__(self, model, producent):
        super().__init__(model, producent)

#TESTOWANIE wielodziedziczenia:

telefon = Smartfon("Galaxy S10", "Samsung")
telefon.wyslij_wiadomosc("Jan Kowalski", "Cześć Janek!")
telefon.odtworz_muzyke("Bohemian Rhapsody")
print("Producent telefonu to:", telefon.producent)
print("Model telefonu to: ", telefon.model)