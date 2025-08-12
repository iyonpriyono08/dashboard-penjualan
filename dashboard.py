import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Connect ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Ambil data dari sheet "Stock"
df = conn.read(worksheet="Stock", usecols=[0,1,2,3,4], ttl=5)
df = df.fillna(0)

st.title("📊 Sales Dashboard")

# Tampilkan tabel stok
st.subheader("Current Stock")
st.dataframe(df)

# Form input penjualan
st.subheader("Record a Sale")
item_list = df["Item"].tolist()
item = st.selectbox("Select Item", item_list)
qty = st.number_input("Quantity Sold", min_value=1)

if st.button("Submit Sale"):
    idx = df[df["Item"] == item].index[0]
    df.loc[idx, "Stock"] -= qty
    df.loc[idx, "Sold"] += qty
    df.loc[idx, "Revenue"] = df.loc[idx, "Sold"] * df.loc[idx, "Price"]

    # Update data di Google Sheets
    conn.update(worksheet="Stock", data=df)
    st.success(f"Sale recorded for {item}!")

# Grafik pendapatan
st.subheader("Monthly Revenue")
st.bar_chart(df.set_index("Item")["Revenue"])
