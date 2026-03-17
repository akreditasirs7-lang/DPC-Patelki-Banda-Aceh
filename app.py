import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# AUTH GOOGLE SHEET
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# OPEN SHEET
sheet = client.open_by_key("1FSBFgihi7edyLmV66XoD7bnoFyL-tkZ1mBdVm5x26jA").sheet1

st.title("Dashboard Input Data Staff")

# FORM INPUT
with st.form("form_data"):
    nama = st.text_input("Nama")
    nomor_str = st.text_input("Nomor STR")
    no_kta = st.text_input("No KTA")
    status = st.text_input("Status Pekerjaan")
    instansi = st.text_input("Instansi")
    gaji = st.text_input("Gaji")
    kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki","Perempuan"])
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    tgl = st.date_input("Tanggal Lahir")

    submit = st.form_submit_button("Simpan")

# FUNGSI CEK & UPDATE
if submit:

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    if not df.empty and no_kta in df["No KTA"].values:

        # UPDATE
        row_index = df[df["No KTA"] == no_kta].index[0] + 2

        sheet.update(f"A{row_index}:J{row_index}", [[
            nama, nomor_str, no_kta, status,
            instansi, gaji, kelamin,
            phone, email, str(tgl)
        ]])

        st.success("Data diupdate!")

    else:

        # INSERT
        sheet.append_row([
            nama, nomor_str, no_kta, status,
            instansi, gaji, kelamin,
            phone, email, str(tgl)
        ])

        st.success("Data ditambahkan!")

# TAMPIL DATA
st.subheader("Data Staff")

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.dataframe(df)
