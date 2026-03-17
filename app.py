import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ===== CONFIG =====
st.set_page_config(layout="wide")

# ===== STYLE (DARK NEON) =====
st.markdown("""
<style>
body {
    background-color: #060e18;
}
.stApp {
    background: linear-gradient(170deg, #060e18, #0a1a2a, #0d1f30);
    color: #e0f0e8;
}

.card {
    background: linear-gradient(135deg, rgba(15,25,40,0.9), rgba(10,20,35,0.95));
    border: 1px solid rgba(0,255,136,0.2);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

.title {
    color: #00ff88;
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===== AUTH =====
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# ===== SHEET =====
SHEET_ID = "1FSBFgihi7edyLmV66XoD7bnoFyL-tkZ1mBdVm5x26jA"
sheet = client.open_by_key(SHEET_ID).worksheet("Sheet1")

# ===== LOAD DATA =====
data = sheet.get_all_records()
df = pd.DataFrame(data)

# ===== HEADER =====
st.markdown('<div class="title">🧪 LABORATORIUM DASHBOARD</div>', unsafe_allow_html=True)
st.caption("Sistem Manajemen Data Staff")

# ===== STATS =====
col1, col2, col3, col4 = st.columns(4)

total = len(df)
aktif = len(df[df["Status"] == "PNS"]) if not df.empty else 0
instansi = df["Instansi"].nunique() if not df.empty else 0

col1.markdown(f'<div class="card"><h4>Total Staff</h4><h2>{total}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h4>Aktif</h4><h2>{aktif}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h4>Rata Gaji</h4><h2>-</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="card"><h4>Instansi</h4><h2>{instansi}</h2></div>', unsafe_allow_html=True)

st.divider()

# ===== CHART =====
colA, colB = st.columns(2)

if not df.empty:

    with colA:
        st.subheader("Distribusi Instansi")
        st.bar_chart(df["Instansi"].value_counts())

    with colB:
        st.subheader("Jenis Kelamin")
        st.bar_chart(df["Jenis Kelamin"].value_counts())

# ===== FORM =====
st.subheader("➕ Tambah Data")

with st.form("form"):

    nama = st.text_input("Nama")
    nomor_str = st.text_input("Nomor STR")
    no_kta = st.text_input("No KTA")
    status = st.selectbox("Status", ["PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"])
    instansi_input = st.text_input("Instansi")

    gaji_map = {
        "Rp 1-4 Juta": "1000000-4000000",
        "Rp 4-6 Juta": "4000000-6000000",
        "> Rp 6 Juta": "6000000+"
    }

    label = st.selectbox("Gaji", list(gaji_map.keys()))
    gaji = gaji_map[label]

    kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    tanggal_lahir = st.date_input("Tanggal Lahir")

    submit = st.form_submit_button("Simpan")

if submit:

    sheet.append_row([
        nama,
        nomor_str,
        no_kta,
        status,
        instansi_input,
        gaji,
        kelamin,
        phone,
        email,
        str(tanggal_lahir)
    ])

    st.success("✅ Data masuk!")
    st.rerun()

# ===== TABLE =====
st.subheader("📋 Data Staff")

if df.empty:
    st.info("Belum ada data")
else:
    st.dataframe(df, use_container_width=True)
