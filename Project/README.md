# Przepiśnik

Prosta aplikacja webowa do przechowywania, przeglądania i edytowania przepisów kulinarnych.
Możesz dodawać własne przepisy, oznaczać je jako ulubione, filtrować po tagach i czasie przygotowania, a nawet wylosować przepis dnia, jeśli nie masz pomysłu, co ugotować.
Przepiśnik to taka osobista książka kucharska w przeglądarce.

## Funkcje aplikacji

- Dodawanie przepisów (tytuł, składniki, instrukcje, czas, tagi)
- Edycja i usuwanie przepisów
- Oznaczanie jako ulubione
- Filtrowanie i wyszukiwanie
- Dashboard z licznikiem i losowym przepisem dnia

## Jak uruchomić lokalnie

1. Sklonuj repozytorium (albo pobierz zipa):
   ```bash
   git clone https://github.com/gorzela31/HighLevelProgrammingII.git
   cd HighLevelProgrammingII/Project
   ```

2. Stwórz i aktywuj wirtualne środowisko:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   ```

3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

4. Uruchom aplikację:
   ```bash
   streamlit run app.py
   ```
   Otwórz w przeglądarce: http://localhost:8501

## Jak zbudować i uruchomić w Dockerze

1. Zbuduj obraz:
   ```bash
   docker build -t przepisnik .
   ```

2. Uruchom kontener:
   ```bash
   docker run --rm -p 8501:8501 przepisnik
   ```
   Aplikacja będzie dostępna pod adresem http://localhost:8501
