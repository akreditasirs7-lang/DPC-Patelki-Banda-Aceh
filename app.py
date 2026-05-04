import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import uuid
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Status Iuran DPC", page_icon="📊", layout="wide")

# --- INISIALISASI KONEKSI GOOGLE SHEETS ---
# Pastikan st.secrets sudah diatur
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Gagal terhubung ke Google Sheets. Pastikan secrets.toml sudah dikonfigurasi dengan benar.")
    st.stop()

# Fungsi untuk mengambil data
@st.cache_data(ttl=5) # Cache data selama 5 detik
def load_data():
    try:
        # Mengambil data dari worksheet pertama (pastikan Google Sheet tidak kosong)
        df = conn.read(worksheet="Data Iuran", usecols=[0, 1, 2, 3]) 
        # Coba paksa tipe data jika kosong
        if df.empty:
            df = pd.DataFrame(columns=["ID", "Nama", "Lunas_Tahun", "Tidak_Lunas_Tahun"])
        else:
            # Pastikan kolom-kolom penting ada
            expected_cols = ["ID", "Nama", "Lunas_Tahun", "Tidak_Lunas_Tahun"]
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = ""
        return df.dropna(how="all") # Hapus baris yang kosong semua
    except Exception as e:
        # Tampilkan error asli agar mudah di-debug
        st.error(f"Error membaca sheet: {e}")
        return pd.DataFrame(columns=["ID", "Nama", "Lunas_Tahun", "Tidak_Lunas_Tahun"])

# --- SISTEM LOGIN ADMIN ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["admin"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password Admin", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Password Admin", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password salah")
        return False
    else:
        # Password correct.
        return True

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Dashboard Utama", "Form Pendaftaran Anggota", "Panel Admin"])

# --- HALAMAN DASHBOARD (PUBLIK) ---
if menu == "Dashboard Utama":
    st.title("📊 Dashboard Status Iuran DPC")
    st.markdown("Cari status iuran anggota dengan mengetikkan nama di bawah ini.")

    df = load_data()
    
    if df.empty:
        st.info("Belum ada data iuran yang tersimpan. Admin perlu menambahkan data terlebih dahulu.")
    else:
        # Fitur Pencarian
        search_query = st.text_input("🔍 Cari Nama Anggota:", "")
        
        if search_query:
            # Filter DataFrame berdasarkan nama (case-insensitive)
            # Pastikan kolom Nama bertipe string dan handle NaN
            df['Nama'] = df['Nama'].astype(str)
            filtered_df = df[df['Nama'].str.contains(search_query, case=False, na=False)]
            
            if filtered_df.empty:
                st.warning(f"Data untuk '{search_query}' tidak ditemukan.")
            else:
                st.success(f"Ditemukan {len(filtered_df)} data.")
                # Tampilkan hasil tanpa index dan ID
                st.dataframe(
                    filtered_df[["Nama", "Lunas_Tahun", "Tidak_Lunas_Tahun"]],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            # Tampilkan semua data jika tidak ada pencarian
            st.dataframe(
                df[["Nama", "Lunas_Tahun", "Tidak_Lunas_Tahun"]],
                use_container_width=True,
                hide_index=True
            )

# --- HALAMAN FORM PENDAFTARAN ANGGOTA ---
elif menu == "Form Pendaftaran Anggota":
    st.title("📝 Form Pendaftaran Anggota")
    st.markdown("Silakan isi data diri Anda pada form di bawah ini.")
    
    with st.form("form_pendaftaran"):
        st.subheader("Data Pribadi")
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *")
            jenis_kelamin = st.selectbox("Jenis Kelamin *", ["-- Pilih --", "Laki-laki", "Perempuan"])
            tanggal_lahir = st.date_input("Tanggal Lahir *", value=datetime.date(1990, 1, 1), min_value=datetime.date(1940, 1, 1))
            no_hp = st.text_input("No. HP *")
            email = st.text_input("Email *")
            
        with col2:
            nomor_str = st.text_input("Nomor STR *")
            no_kta = st.text_input("No. KTA *")
            status_pekerjaan = st.selectbox("Status Pekerjaan *", ["-- Pilih --", "PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"])
            instansi = st.text_input("Instansi / Tempat Kerja *")
            gaji = st.selectbox("Rentang Gaji *", ["-- Pilih --", "Rp 1.000.000 s.d Rp 3.000.000", "Rp 3.000.000 s.d Rp 5.000.000", "> Rp 5.000.000"])
            status_anggota = st.selectbox("Status Keanggotaan *", ["-- Pilih --", "Aktif", "Tidak Aktif"])
            
        st.markdown("*Wajib diisi")
        submit_daftar = st.form_submit_button("Simpan Data Pendaftaran", type="primary")
        
        if submit_daftar:
            if not nama or jenis_kelamin == "-- Pilih --" or not nomor_str or not no_kta or status_pekerjaan == "-- Pilih --" or not instansi or gaji == "-- Pilih --" or not no_hp or not email or status_anggota == "-- Pilih --":
                st.error("Semua kolom bertanda bintang (*) wajib diisi/dipilih!")
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tgl_lahir_str = tanggal_lahir.strftime("%Y-%m-%d")
                
                new_anggota = pd.DataFrame([{
                    "Timestamp": timestamp,
                    "Nama": nama,
                    "Jenis Kelamin": jenis_kelamin,
                    "Tgl Lahir": tgl_lahir_str,
                    "No STR": nomor_str,
                    "No KTA": no_kta,
                    "Status Kerja": status_pekerjaan,
                    "Instansi": instansi,
                    "Gaji": gaji,
                    "No HP": no_hp,
                    "Email": email,
                    "Status": status_anggota
                }])
                
                # Ambil data lama dari worksheet "Data Anggota"
                try:
                    df_anggota = conn.read(worksheet="Data Anggota", dtype=str)
                    if df_anggota.empty:
                        df_anggota = pd.DataFrame(columns=new_anggota.columns)
                    else:
                        df_anggota = df_anggota.dropna(how="all")
                except Exception:
                    df_anggota = pd.DataFrame(columns=new_anggota.columns)
                
                # Gabungkan data
                updated_anggota = pd.concat([df_anggota, new_anggota], ignore_index=True)
                
                # Simpan ke Google Sheets
                try:
                    conn.update(worksheet="Data Anggota", data=updated_anggota)
                    st.success(f"Terima kasih {nama}! Data pendaftaran Anda berhasil disimpan.")
                except Exception as e:
                    st.error(f"Gagal menyimpan data ke Google Sheets. Pastikan Anda sudah membuat tab bernama 'Data Anggota' di file Google Sheets Anda. Detail error: {e}")

# --- HALAMAN PANEL ADMIN ---
elif menu == "Panel Admin":
    st.title("⚙️ Panel Admin")
    
    # Proteksi Halaman Admin
    if not check_password():
        st.stop()  # Hentikan eksekusi jika belum login
    
    st.success("Berhasil login sebagai Admin!")
    
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    df = load_data()

    # Tab untuk Manajemen Data
    tab1, tab2, tab3 = st.tabs(["➕ Tambah Data", "✏️ Edit Data", "🗑️ Hapus Data"])

    # --- TAB TAMBAH DATA ---
    with tab1:
        st.subheader("Tambah Data Iuran Baru")
        with st.form("form_tambah"):
            nama_baru = st.text_input("Nama Anggota")
            lunas_baru = st.text_input("Status Lunas (Contoh: 2020-2023)")
            tidak_lunas_baru = st.text_input("Status Tidak Lunas (Contoh: 2024)")
            
            submit_tambah = st.form_submit_button("Simpan Data")
            
            if submit_tambah:
                if not nama_baru:
                    st.error("Nama tidak boleh kosong!")
                else:
                    new_id = str(uuid.uuid4())[:8] # Buat ID unik 8 karakter
                    new_row = pd.DataFrame([{
                        "ID": new_id,
                        "Nama": nama_baru,
                        "Lunas_Tahun": lunas_baru,
                        "Tidak_Lunas_Tahun": tidak_lunas_baru
                    }])
                    
                    # Gabungkan dengan data lama
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    
                    # Update ke Google Sheets
                    try:
                        conn.update(worksheet="Data Iuran", data=updated_df)
                        st.cache_data.clear() # Bersihkan cache agar data terbaru langsung termuat
                        st.success(f"Data {nama_baru} berhasil ditambahkan!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menyimpan data: {e}")

    # --- TAB EDIT DATA ---
    with tab2:
        st.subheader("Edit Data Iuran")
        if df.empty:
            st.info("Tidak ada data untuk diedit.")
        else:
            # Pilih data yang mau diedit
            opsi_edit = df['Nama'].astype(str) + " (ID: " + df['ID'].astype(str) + ")"
            pilihan = st.selectbox("Pilih Data yang Akan Diedit:", opsi_edit)
            
            if pilihan:
                # Cari ID dari string pilihan
                selected_id = pilihan.split("(ID: ")[1].replace(")", "")
                data_terpilih = df[df['ID'].astype(str) == selected_id].iloc[0]
                
                with st.form("form_edit"):
                    edit_nama = st.text_input("Nama Anggota", value=str(data_terpilih['Nama']) if not pd.isna(data_terpilih['Nama']) else "")
                    # Handle NaN values for text inputs
                    val_lunas = "" if pd.isna(data_terpilih['Lunas_Tahun']) else str(data_terpilih['Lunas_Tahun'])
                    val_tidak_lunas = "" if pd.isna(data_terpilih['Tidak_Lunas_Tahun']) else str(data_terpilih['Tidak_Lunas_Tahun'])
                    
                    edit_lunas = st.text_input("Status Lunas", value=val_lunas)
                    edit_tidak_lunas = st.text_input("Status Tidak Lunas", value=val_tidak_lunas)
                    
                    submit_edit = st.form_submit_button("Update Data")
                    
                    if submit_edit:
                        if not edit_nama:
                            st.error("Nama tidak boleh kosong!")
                        else:
                            # Update nilai di dataframe
                            idx = df.index[df['ID'].astype(str) == selected_id].tolist()[0]
                            df.at[idx, 'Nama'] = edit_nama
                            df.at[idx, 'Lunas_Tahun'] = edit_lunas
                            df.at[idx, 'Tidak_Lunas_Tahun'] = edit_tidak_lunas
                            
                            # Simpan ke Google Sheets
                            try:
                                conn.update(worksheet="Data Iuran", data=df)
                                st.cache_data.clear()
                                st.success("Data berhasil diupdate!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Gagal mengupdate data: {e}")

    # --- TAB HAPUS DATA ---
    with tab3:
        st.subheader("Hapus Data Iuran")
        if df.empty:
            st.info("Tidak ada data untuk dihapus.")
        else:
            opsi_hapus = df['Nama'].astype(str) + " (ID: " + df['ID'].astype(str) + ")"
            pilihan_hapus = st.selectbox("Pilih Data yang Akan Dihapus:", opsi_hapus)
            
            if pilihan_hapus:
                selected_id_hapus = pilihan_hapus.split("(ID: ")[1].replace(")", "")
                
                st.warning(f"Apakah Anda yakin ingin menghapus data **{pilihan_hapus}**?")
                if st.button("Ya, Hapus Data", type="primary"):
                    # Hapus baris dari dataframe
                    df = df[df['ID'].astype(str) != selected_id_hapus]
                    
                    # Simpan ulang ke Google Sheets
                    try:
                        conn.update(worksheet="Data Iuran", data=df)
                        st.cache_data.clear()
                        st.success("Data berhasil dihapus!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghapus data: {e}")
