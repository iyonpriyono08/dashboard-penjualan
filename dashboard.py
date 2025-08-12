import pandas as pd
import streamlit as st
import plotly.express as px

# URL CSV Google Sheet
# Ganti dengan URL CSV hasil "Publish to the web"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9GM2tHh38T7TQeAw8myUrJxWsSu4B2m33Omt27sWfnRoNs_qMjHl46YZjCEGpD6kAoy3eb1nwE30Z/pub?gid=0&single=true&output=csv"

# Load data dari Google Sheet
df = pd.read_csv(SHEET_URL)

# Judul Dashboard
st.title("📊 Dashboard Penjualan & Stok")

# Tampilkan tabel
st.subheader("Data Penjualan")
st.dataframe(df)

# Grafik Pendapatan
fig1 = px.bar(
    df,
    x="Produk",
    y="Pendapatan",
    color="Produk",
    title="Pendapatan per Produk",
    text_auto=True
)
st.plotly_chart(fig1)

# Grafik Stok Tersisa
fig2 = px.bar(
    df,
    x="Produk",
    y="Stok Tersisa",
    color="Produk",
    title="Sisa Stok per Produk",
    text_auto=True
)
st.plotly_chart(fig2)

# Grafik Tren Penjualan berdasarkan tanggal
fig3 = px.line(
    df,
    x="Tanggal",
    y="Pendapatan",
    color="Produk",
    markers=True,
    title="Tren Pendapatan Harian"
)
st.plotly_chart(fig3)

st.caption("📌 Data diperbarui otomatis dari Google Sheet setiap kali ada perubahan.")
