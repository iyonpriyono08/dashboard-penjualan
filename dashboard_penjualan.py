import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Load credentials dari secrets
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_credentials"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)

# Ambil Spreadsheet
SHEET_ID = st.secrets["SPREADSHEET_ID"]
spreadsheet = client.open_by_key(SHEET_ID)

# Sheet stok & transaksi
stok_sheet = spreadsheet.worksheet("stok")
transaksi_sheet = spreadsheet.worksheet("transaksi")

# Fungsi baca stok
def load_stok():
    df = pd.DataFrame(stok_sheet.get_all_records())
    return df

# Fungsi update stok & tambah transaksi
def add_transaction(item, qty):
    df = load_stok()
    if item not in df["Item"].values:
        st.error("Item tidak ditemukan!")
        return
    idx = df[df["Item"] == item].index[0]
    if df.loc[idx, "Stok"] < qty:
        st.error("Stok tidak cukup!")
        return
    # Kurangi stok
    df.loc[idx, "Stok"] -= qty
    stok_sheet.update_cell(idx+2, 3, df.loc[idx, "Stok"])
    # Tambah transaksi
    harga_total = qty * df.loc[idx, "Harga"]
    transaksi_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        item,
        qty,
        harga_total
    ])
    st.success(f"Berhasil menambahkan pembelian {qty} {item}")

# Fungsi hitung pendapatan bulanan
def monthly_revenue():
    df = pd.DataFrame(transaksi_sheet.get_all_records())
    if df.empty:
        return pd.DataFrame(columns=["Item", "Pendapatan"])
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    this_month = df[df["Tanggal"].dt.month == datetime.now().month]
    revenue = this_month.groupby("Item")["Harga Total"].sum().reset_index()
    revenue.rename(columns={"Harga Total": "Pendapatan"}, inplace=True)
    return revenue

# UI Streamlit
st.title("📦 Dashboard Penjualan")

menu = st.sidebar.radio("Menu", ["Lihat Stok", "Input Penjualan", "Pendapatan Bulanan"])

if menu == "Lihat Stok":
    st.subheader("Sisa Stok")
    st.dataframe(load_stok())

elif menu == "Input Penjualan":
    st.subheader("Tambah Penjualan")
    stok_df = load_stok()
    item = st.selectbox("Pilih Item", stok_df["Item"])
    qty = st.number_input("Jumlah", min_value=1, step=1)
    if st.button("Simpan"):
        add_transaction(item, qty)

elif menu == "Pendapatan Bulanan":
    st.subheader("Pendapatan Bulan Ini")
    st.dataframe(monthly_revenue())
