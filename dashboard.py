import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURASI ---
st.set_page_config(page_title="📊 Dashboard Penjualan", layout="wide")

# --- URL Google Sheet (Ganti dengan punyamu) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1k9Orw5Cr17DgoHj0XaYsGPHAeBd0xGA4aSjyJ8lC-Kc/edit?usp=sharing"
CSV_URL = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")

# --- LOAD DATA ---
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(CSV_URL)
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# --- TAMPILKAN DATA ---
st.title("📊 Dashboard Penjualan")
st.dataframe(df, use_container_width=True)

# Pastikan kolom ada
required_columns = {"Tanggal", "Produk", "Jumlah", "Pendapatan"}
if not required_columns.issubset(df.columns):
    st.error(f"Kolom wajib tidak lengkap. Harus ada: {', '.join(required_columns)}")
    st.stop()

# --- KONVERSI TIPE DATA ---
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

# --- METRIK UTAMA ---
total_penjualan = df["Jumlah"].sum()
total_pendapatan = df["Pendapatan"].sum()
produk_terlaris = df.groupby("Produk")["Jumlah"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Unit Terjual", f"{total_penjualan:,}")
col2.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
col3.metric("Produk Terlaris", produk_terlaris)

# --- GRAFIK PENJUALAN PER HARI ---
penjualan_per_hari = df.groupby("Tanggal").agg({"Jumlah": "sum"}).reset_index()
fig1 = px.line(p

