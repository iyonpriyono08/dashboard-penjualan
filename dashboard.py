import streamlit as st
import pandas as pd
import requests
from datetime import datetime

API_URL = "https://script.google.com/macros/s/AKfycby0AnsebkkN3hRk3LUyWi3VXiwWRenqS1KZePf7ru6f8rXxTzoColoOC8zvmTHKzB4yMg/exec"  # Ganti dengan URL dari Google Apps Script

st.title("📊 Dashboard Penjualan")

# Fungsi ambil data
@st.cache_data(ttl=60)
def load_data():
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])  # row pertama = header
    df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce")
    df["Jumlah Terjual"] = pd.to_numeric(df["Jumlah Terjual"], errors="coerce")
    df["Pendapatan"] = df["Harga"] * df["Jumlah Terjual"]
    return df

# Tampilkan data
df = load_data()
st.dataframe(df)

# Tambah transaksi baru
st.subheader("➕ Tambah Transaksi")
produk = st.text_input("Nama Produk")
harga = st.number_input("Harga", min_value=0)
stok = st.number_input("Stok", min_value=0)
terjual = st.number_input("Jumlah Terjual", min_value=0)

if st.button("Simpan"):
    today = datetime.now().strftime("%Y-%m-%d")
    pendapatan = harga * terjual
    row = [today, produk, harga, stok, terjual, pendapatan]
    requests.post(API_URL, json=row)
    st.success("Transaksi berhasil disimpan!")
    st.cache_data.clear()

# Statistik
st.subheader("📈 Statistik")
st.write(f"Total Pendapatan: Rp {df['Pendapatan'].sum():,.0f}")

