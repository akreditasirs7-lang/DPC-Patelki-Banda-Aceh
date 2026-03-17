import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
# ===== AUTH GOOGLE SHEETS (PAKAI SECRETS) =====
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
client = gspread.authorize(creds)

# ===== OPEN GOOGLE SHEET =====
SHEET_ID = "1FSBFgihi7edyLmV66XoD7bnoFyL-tkZ1mBdVm5x26jA" 
sheet = client.open_by_key(SHEET_ID).worksheet("Sheet1")

# ===== UI =====
st.title("📊 Dashboard Data Staff")

# ===== FORM INPUT =====
with st.form("form_input"):

    nama = st.text_input("Nama")
    nomor_str = st.text_input("Nomor STR")
    no_kta = st.text_input("No KTA")
    status = st.selectbox("Status Pekerjaan", ["", "PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"])
    instansi = st.text_input("Instansi")
    gaji = st.text_input("Gaji")
    kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    tanggal_lahir = st.date_input("Tanggal Lahir")

    submit = st.form_submit_button("💾 Simpan Data")

# ===== LOGIC INSERT / UPDATE =====
if submit:

    if not nama or not no_kta:
        st.error("Nama dan No KTA wajib diisi!")
    else:

        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if not df.empty and no_kta in df["No KTA"].values:

            # UPDATE DATA
            row_index = df[df["No KTA"] == no_kta].index[0] + 2

            sheet.update(f"A{row_index}:J{row_index}", [[
                nama,
                nomor_str,
                no_kta,
                status,
                instansi,
                gaji,
                kelamin,
                phone,
                email,
                str(tanggal_lahir)
            ]])

            st.success("✅ Data berhasil diupdate!")

        else:

            # INSERT DATA
            sheet.append_row([
                nama,
                nomor_str,
                no_kta,
                status,
                instansi,
                gaji,
                kelamin,
                phone,
                email,
                str(tanggal_lahir)
            ])

            st.success("✅ Data berhasil ditambahkan!")

# ===== TAMPIL DATA =====
st.subheader("📋 Data Staff")

data = sheet.get_all_records()
df = pd.DataFrame(data)

if df.empty:
    st.info("Belum ada data")
else:
    st.dataframe(df, use_container_width=True)

# ===== REFRESH BUTTON =====
if st.button("🔄 Refresh Data"):
    st.rerun()
