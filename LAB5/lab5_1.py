import sqlite3

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM sales")
rows = cursor.fetchall()

for row in rows:
    print(row)

# a) Wyświetl tylko sprzedaż produktu „Laptop”
print("\nWyświetl tylko sprzedaż produktu Laptop")
cursor.execute("SELECT * FROM sales WHERE product = 'Laptop'")
rows = cursor.fetchall() 
for row in rows:
    print(row)

# b) Wyświetl dane tylko z dni 2025-05-07 i 2025-05-08
print("\nWyświetl dane tylko z dni 2025-05-07 i 2025-05-08")
cursor.execute("SELECT * FROM sales WHERE date IN ('2025-05-07', '2025-05-08')")
rows = cursor.fetchall()
for row in rows:
    print(row)

# c) Wyświetl tylko transakcje, w których cena jednostkowa przekracza 200 zł
print("\nWyświetl tylko transakcje, w których cena jednostkowa przekracza 200 zł")
cursor.execute("SELECT * FROM sales WHERE price > 200")
rows = cursor.fetchall()
for row in rows:
    print(row)

# d) Oblicz łączną wartość sprzedaży dla każdego produktu
print("\nŁączna wartość sprzedaży dla każdego produktu")
cursor.execute("SELECT product, SUM(price * quantity) as total_sales FROM sales GROUP BY product")
rows = cursor.fetchall()
for row in rows:
    print(f"Produkt: {row[0]}, Łączna sprzedaż: {row[1]}")


# e) Znajdź dzień z największą liczbą sprzedanych sztuk
print("\nDzień z największą liczbą sprzedanych sztuk")
cursor.execute("SELECT date, SUM(quantity) as total_quantity FROM sales GROUP BY date ORDER BY total_quantity DESC LIMIT 1")
row = cursor.fetchone()
if row:
    print(f"Data: {row[0]}, Liczba sprzedanych sztuk: {row[1]}")

conn.close()