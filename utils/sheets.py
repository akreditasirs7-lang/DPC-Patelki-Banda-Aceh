import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_ANGGOTA = "Data Anggota"
SHEET_IURAN   = "Data Iuran"

HEADER_ANGGOTA = [
    "Timestamp", "Nama", "Jenis Kelamin", "Tanggal Lahir",
    "Nomor STR", "No KTA", "Status Pekerjaan", "Instansi",
    "Gaji", "No HP", "Email", "Status Keanggotaan"
]
HEADER_IURAN = [
    "No KTA", "Nama", "Tahun Dari", "Tahun Sampai", "Status Iuran", "Diperbarui"
]


@st.cache_resource(ttl=300)
def get_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return gspread.authorize(creds)


def get_spreadsheet():
    gc = get_client()
    return gc.open_by_key(st.secrets["sheets"]["spreadsheet_id"])


def _get_or_create_sheet(ss, name, headers):
    try:
        ws = ss.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet(title=name, rows=1000, cols=len(headers))
        ws.append_row(headers)
    return ws


# ── ANGGOTA ──────────────────────────────────────────────────
def load_anggota() -> pd.DataFrame:
    try:
        ss = get_spreadsheet()
        ws = _get_or_create_sheet(ss, SHEET_ANGGOTA, HEADER_ANGGOTA)
        data = ws.get_all_records()
        if not data:
            return pd.DataFrame(columns=HEADER_ANGGOTA)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Gagal memuat data anggota: {e}")
        return pd.DataFrame(columns=HEADER_ANGGOTA)


def tambah_anggota(row: dict) -> bool:
    try:
        ss = get_spreadsheet()
        ws = _get_or_create_sheet(ss, SHEET_ANGGOTA, HEADER_ANGGOTA)
        from datetime import datetime
        ws.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row["nama"], row["jenis_kelamin"], row["tanggal_lahir"],
            row["nomor_str"], row["no_kta"], row["status_pekerjaan"],
            row["instansi"], row["gaji"], row["phone"],
            row["email"], row["status"]
        ])
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan: {e}")
        return False


def hapus_anggota(no_kta: str) -> bool:
    try:
        ss = get_spreadsheet()
        ws = ss.worksheet(SHEET_ANGGOTA)
        cell = ws.find(no_kta, in_column=6)
        if cell:
            ws.delete_rows(cell.row)
            return True
        return False
    except Exception as e:
        st.error(f"Gagal menghapus: {e}")
        return False


# ── IURAN ────────────────────────────────────────────────────
def load_iuran() -> pd.DataFrame:
    try:
        ss = get_spreadsheet()
        ws = _get_or_create_sheet(ss, SHEET_IURAN, HEADER_IURAN)
        data = ws.get_all_records()
        if not data:
            return pd.DataFrame(columns=HEADER_IURAN)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Gagal memuat data iuran: {e}")
        return pd.DataFrame(columns=HEADER_IURAN)


def simpan_iuran(row: dict) -> bool:
    try:
        ss = get_spreadsheet()
        ws = _get_or_create_sheet(ss, SHEET_IURAN, HEADER_IURAN)
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ambil semua data
        all_values = ws.get_all_values()
        
        # Cari baris yang no_kta-nya cocok (mulai baris ke-2, index 1)
        found_row = None
        for i, row_data in enumerate(all_values):
            if i == 0:
                continue  # skip header
            if str(row_data[0]).strip() == str(row["no_kta"]).strip():
                found_row = i + 1  # nomor baris di Sheets (1-based)
                break

        new_data = [
            str(row["no_kta"]),
            str(row["nama"]),
            str(row["tahun_dari"]),
            str(row["tahun_sampai"]),
            str(row["status_iuran"]),
            now
        ]

        if found_row:
            # Update baris yang ada
            ws.update(f"A{found_row}:F{found_row}", [new_data])
        else:
            # Tambah baris baru
            ws.append_row(new_data)

        return True
    except Exception as e:
        st.error(f"Gagal menyimpan iuran: {e}")
        return False


def hapus_iuran(no_kta: str) -> bool:
    try:
        ss = get_spreadsheet()
        ws = ss.worksheet(SHEET_IURAN)
        cell = ws.find(no_kta, in_column=1)
        if cell:
            ws.delete_rows(cell.row)
            return True
        return False
    except Exception as e:
        st.error(f"Gagal menghapus iuran: {e}")
        return False
