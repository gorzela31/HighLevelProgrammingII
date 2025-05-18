import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Połączenie z bazą danych
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

st.title("Sales Dashboard")

# Sekcja dodawania nowej sprzedaży
st.header("Dodaj nową sprzedaż")
product = st.text_input("Produkt")
quantity = st.number_input("Ilość", min_value=1, step=1)
price = st.number_input("Cena jednostkowa", min_value=0.0, step=0.1)
date = st.date_input("Data sprzedaży")

if st.button("Dodaj sprzedaż"):
    cursor.execute("INSERT INTO sales (product, quantity, price, date) VALUES (?, ?, ?, ?)",(product, quantity, price, date.strftime("%Y-%m-%d")))
    conn.commit()
    st.success("✅ Sprzedaż dodana pomyślnie!")
    st.balloons()

# Wczytanie danych
sales_df = pd.read_sql_query("SELECT * FROM sales", conn)

# Filtrowanie
st.header("Dane sprzedażowe")
unique_products = sales_df["product"].unique()
selected_product = st.selectbox("Wybierz produkt do filtrowania", options=["Wszystkie"] + list(unique_products))

if selected_product != "Wszystkie":
    filtered_df = sales_df[sales_df["product"] == selected_product]
else:
    filtered_df = sales_df

st.dataframe(filtered_df)

# Wykresy
st.header("Analiza sprzedaży")

# Wykres dzienny: wartość sprzedaży
sales_df["value"] = sales_df["quantity"] * sales_df["price"]
daily_sales = sales_df.groupby("date")["value"].sum().reset_index()

fig1, ax1 = plt.subplots()
ax1.plot(daily_sales["date"], daily_sales["value"], marker='o')
ax1.set_title("Sprzedaż dzienna (wartość)")
ax1.set_xlabel("Data")
ax1.set_ylabel("Wartość sprzedaży")
st.pyplot(fig1)

# Wykres suma produktów wg typu
product_summary = sales_df.groupby("product")["quantity"].sum().reset_index()
fig2, ax2 = plt.subplots()
ax2.bar(product_summary["product"], product_summary["quantity"])
ax2.set_title("Suma sprzedanych produktów wg typu")
ax2.set_xlabel("Produkt")
ax2.set_ylabel("Suma ilości")
st.pyplot(fig2)

conn.close()

#python -m streamlit run lab5_2.py <- to be used in terminal to run the app
