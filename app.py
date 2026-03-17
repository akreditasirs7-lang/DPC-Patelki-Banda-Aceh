import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ===== CONFIG =====
st.set_page_config(layout="wide")

# ===== STATE =====
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# ===== STYLE =====
st.markdown("""
<style>
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
col1, col2 = st.columns([8,1])

with col1:
    st.markdown('<div class="title">🧪 LABORATORIUM DASHBOARD</div>', unsafe_allow_html=True)

with col2:
    if st.button("➕ Tambah"):
        st.session_state.show_form = True
        st.session_state.edit_index = None

st.caption("Sistem Manajemen Data Staff")

# ===== FILTER =====
st.subheader("🔍 Filter")

colf1, colf2 = st.columns(2)

with colf1:
    search = st.text_input("Cari Nama")

with colf2:
    status_filter = st.selectbox("Filter Status", ["Semua", "PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"])

df_filtered = df.copy()

if not df_filtered.empty:

    if search:
        df_filtered = df_filtered[df_filtered["Nama"].str.contains(search, case=False, na=False)]

    if status_filter != "Semua":
        df_filtered = df_filtered[df_filtered["Status"] == status_filter]

# ===== STATS =====
col1, col2, col3, col4 = st.columns(4)

total = len(df_filtered)
aktif = len(df_filtered[df_filtered["Status"] == "PNS"]) if "Status" in df_filtered.columns else 0
instansi = df_filtered["Instansi"].nunique() if "Instansi" in df_filtered.columns else 0

col1.markdown(f'<div class="card"><h4>Total</h4><h2>{total}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h4>Aktif</h4><h2>{aktif}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h4>Instansi</h4><h2>{instansi}</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="card"><h4>Data</h4><h2>{len(df)}</h2></div>', unsafe_allow_html=True)

st.divider()

# ===== TABLE + ACTION =====
st.subheader("📋 Data Staff")

if df_filtered.empty:
    st.info("Tidak ada data")
else:

    for i, row in df_filtered.iterrows():
        col1, col2, col3 = st.columns([6,1,1])

        col1.write(f"**{row['Nama']}** | {row['Status']} | {row['Instansi']}")

        if col2.button("✏️ Edit", key=f"edit_{i}"):
            st.session_state.show_form = True
            st.session_state.edit_index = i

        if col3.button("🗑️ Hapus", key=f"del_{i}"):
            sheet.delete_rows(i + 2)
            st.success("Data dihapus")
            st.rerun()

# ===== FORM =====
if st.session_state.show_form:

    st.markdown("## 📝 Form Data")

    data_edit = None
    if st.session_state.edit_index is not None:
        data_edit = df.iloc[st.session_state.edit_index]

    with st.form("form"):

        nama = st.text_input("Nama", value=data_edit["Nama"] if data_edit is not None else "")
        nomor_str = st.text_input("Nomor STR", value=data_edit["Nomor STR"] if data_edit is not None else "")
        no_kta = st.text_input("No KTA", value=data_edit["No KTA"] if data_edit is not None else "")

        status = st.selectbox("Status", [
            "PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"
        ])

        instansi_input = st.text_input("Instansi", value=data_edit["Instansi"] if data_edit is not None else "")

        gaji_map = {
            "Rp 1-4 Juta": "1000000-4000000",
            "Rp 4-6 Juta": "4000000-6000000",
            "> Rp 6 Juta": "6000000+"
        }

        label = st.selectbox("Gaji", list(gaji_map.keys()))
        gaji = gaji_map[label]

        kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        phone = st.text_input("Phone", value=data_edit["Phone"] if data_edit is not None else "")
        email = st.text_input("Email", value=data_edit["Email"] if data_edit is not None else "")
        tanggal_lahir = st.date_input("Tanggal Lahir")

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 Simpan")

        with col2:
            cancel = st.form_submit_button("❌ Tutup")

        if submit:

            if st.session_state.edit_index is not None:
                row_idx = st.session_state.edit_index + 2

                sheet.update(f"A{row_idx}:J{row_idx}", [[
                    nama, nomor_str, no_kta, status,
                    instansi_input, gaji, kelamin,
                    phone, email, str(tanggal_lahir)
                ]])

                st.success("✅ Data diupdate!")

            else:
                sheet.append_row([
                    nama, nomor_str, no_kta, status,
                    instansi_input, gaji, kelamin,
                    phone, email, str(tanggal_lahir)
                ])

                st.success("✅ Data ditambah!")

            st.session_state.show_form = False
            st.session_state.edit_index = None
            st.rerun()

        if cancel:
            st.session_state.show_form = False
            st.session_state.edit_index = None
            st.rerun()
