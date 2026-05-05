import streamlit as st
import pandas as pd
from datetime import date
from utils.style import inject_css, header_html
from utils.sheets import load_anggota, tambah_anggota, load_iuran

st.set_page_config(
    page_title="DPC Patelki Banda Aceh",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()

# Force transparent background untuk animasi tampil
st.markdown("""
<style>
.stApp {
    background: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}
[data-testid="stMain"] {
    background: transparent !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
section[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(header_html(show_admin_btn=True, is_admin=False), unsafe_allow_html=True)


@st.cache_data(ttl=60)
def get_data():
    return load_anggota(), load_iuran()


df_anggota, df_iuran = get_data()

n_total = len(df_anggota)
status_col_a = next((c for c in ["Status Keanggotaan", "Status", "status"] if c in df_anggota.columns), None)
n_aktif = len(df_anggota[df_anggota[status_col_a] == "Aktif"]) if status_col_a and not df_anggota.empty else 0
n_lunas = len(df_iuran[df_iuran["Status Iuran"] == "Lunas"]) if not df_iuran.empty and "Status Iuran" in df_iuran.columns else 0

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "Total Anggota", n_total, "#F1F5F9", "terdaftar"),
    (c2, "Anggota Aktif", n_aktif, "#34D399", "status aktif"),
    (c3, "Iuran Lunas", n_lunas, "#60A5FA", "anggota lunas"),
    (c4, "Belum Lunas", n_total - n_lunas if n_total else 0, "#FBBF24", "perlu perhatian"),
]
for col, lbl, val, color, sub in cards:
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-lbl">{lbl}</div>
            <div class="stat-val" style="color:{color}">{val}</div>
            <div class="stat-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👥  Data Anggota", "💳  Status Iuran", "➕  Daftar Anggota Baru"])

# ── TAB 1 ──
with tab1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_s, col_b = st.columns([3, 1])
    with col_s:
        search = st.text_input(
            "Cari HP", placeholder="Ketik nomor HP anggota...",
            label_visibility="collapsed"
        )
    with col_b:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    disp = df_anggota.copy()
    if search and not disp.empty:
        disp = disp[disp["No HP"].astype(str).str.contains(search, na=False)]

    if disp.empty:
        st.markdown(
            "<div style='text-align:center;padding:3rem;color:#475569'>🔍 Tidak ada data.</div>",
            unsafe_allow_html=True
        )
    else:
        status_col = next((c for c in ["Status Keanggotaan", "Status", "status"] if c in disp.columns), None)
        cols_show = ["Nama", "No HP", "Nomor STR", "No KTA", "Status Pekerjaan", "Instansi", "Gaji"]
        if status_col:
            cols_show.append(status_col)
        cols_show = [c for c in cols_show if c in disp.columns]
        st.dataframe(disp[cols_show], use_container_width=True, hide_index=True, height=420)
        st.caption(f"Menampilkan {len(disp)} dari {n_total} anggota")

# ── TAB 2 ──
with tab2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    search_i = st.text_input(
        "Cari iuran", placeholder="Ketik nama atau No. KTA...",
        label_visibility="collapsed", key="search_iuran"
    )

    disp_i = df_iuran.copy()
    if search_i and not disp_i.empty:
        mask = (
            disp_i["Nama"].astype(str).str.lower().str.contains(search_i.lower(), na=False) |
            disp_i["No KTA"].astype(str).str.contains(search_i, na=False)
        )
        disp_i = disp_i[mask]

    if disp_i.empty:
        st.markdown(
            "<div style='text-align:center;padding:3rem;color:#475569'>💳 Belum ada data iuran.</div>",
            unsafe_allow_html=True
        )
    else:
        st.dataframe(disp_i, use_container_width=True, hide_index=True, height=400)
        st.caption(f"Menampilkan {len(disp_i)} data iuran")

# ── TAB 3 ──
with tab3:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
        border-radius:10px;padding:12px 16px;font-size:12px;color:#93C5FD;margin-bottom:16px'>
        📋 Lengkapi semua field di bawah untuk mendaftarkan anggota baru.
    </div>""", unsafe_allow_html=True)

    with st.form("form_daftar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *")
            tanggal_lahir = st.date_input("Tanggal Lahir *", min_value=date(1940, 1, 1), max_value=date.today())
            nomor_str = st.text_input("Nomor STR *")
            status_kerja = st.selectbox("Status Pekerjaan *", ["", "PNS", "P3K", "Kontrak", "Bhakti", "Tidak Bekerja"])
            gaji = st.selectbox("Rentang Gaji *", ["", "Rp 1.000.000 s.d Rp 3.000.000", "Rp 3.000.000 s.d Rp 5.000.000", "> Rp 5.000.000"])
            email = st.text_input("Email *")
        with col2:
            jenis_kelamin = st.selectbox("Jenis Kelamin *", ["", "Laki-laki", "Perempuan"])
            no_kta = st.text_input("No. KTA *")
            instansi = st.text_input("Instansi / Tempat Kerja *")
            phone = st.text_input("No. HP *", placeholder="08xxxxxxxxxx")
            status_anggota = st.selectbox("Status Keanggotaan *", ["", "Aktif", "Tidak Aktif"])

        submitted = st.form_submit_button("💾 Simpan Data Anggota", use_container_width=True)

    if submitted:
        missing = [f for f, v in [
            ("Nama", nama), ("Jenis Kelamin", jenis_kelamin), ("No KTA", no_kta),
            ("Nomor STR", nomor_str), ("Status Pekerjaan", status_kerja),
            ("Instansi", instansi), ("Gaji", gaji), ("No HP", phone),
            ("Email", email), ("Status Keanggotaan", status_anggota)
        ] if not v]
        if missing:
            st.error(f"Field berikut wajib diisi: {', '.join(missing)}")
        elif "@" not in email:
            st.error("Format email tidak valid.")
        else:
            ok = tambah_anggota({
                "nama": nama, "jenis_kelamin": jenis_kelamin,
                "tanggal_lahir": str(tanggal_lahir), "nomor_str": nomor_str,
                "no_kta": no_kta, "status_pekerjaan": status_kerja,
                "instansi": instansi, "gaji": gaji, "phone": phone,
                "email": email, "status": status_anggota
            })
            if ok:
                st.success("✅ Data anggota berhasil disimpan!")
                st.cache_data.clear()
            else:
                st.error("❌ Gagal menyimpan. Cek koneksi Google Sheets.")
