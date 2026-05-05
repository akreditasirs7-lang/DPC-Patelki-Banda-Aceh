import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.style import inject_css, header_html
from utils.auth import check_password, login_form, logout
from utils.sheets import (
    load_anggota, load_iuran, simpan_iuran,
    hapus_iuran, hapus_anggota
)

st.set_page_config(
    page_title="Admin — DPC Patelki",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()

if not check_password():
    st.markdown(header_html(show_admin_btn=False, is_admin=False), unsafe_allow_html=True)
    login_form()
    st.stop()

st.markdown(header_html(show_admin_btn=False, is_admin=True), unsafe_allow_html=True)

col_title, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Logout", use_container_width=True):
        logout()

@st.cache_data(ttl=30)
def get_admin_data():
    return load_anggota(), load_iuran()

df_anggota, df_iuran = get_admin_data()

n_total = len(df_anggota)
n_lunas = len(df_iuran[df_iuran["Status Iuran"] == "Lunas"]) if not df_iuran.empty and "Status Iuran" in df_iuran.columns else 0
n_belum = len(df_iuran) - n_lunas

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
for col, lbl, val, color, sub in [
    (c1, "Total Anggota", n_total, "#F1F5F9", "terdaftar"),
    (c2, "Iuran Lunas",   n_lunas, "#60A5FA", "anggota lunas"),
    (c3, "Belum Lunas",   n_belum, "#FBBF24", "perlu ditindak"),
]:
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-lbl">{lbl}</div>
            <div class="stat-val" style="color:{color}">{val}</div>
            <div class="stat-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── FORM SET IURAN ──
st.markdown("""
<div style='background:rgba(30,41,59,.9);border:1px solid rgba(59,130,246,.2);
    border-radius:14px;padding:1rem 1.25rem .5rem;margin-bottom:1rem'>
    <p style='color:#93C5FD;font-size:13px;font-weight:600;margin-bottom:1rem'>
    💳 Set Status Iuran Anggota</p>
</div>""", unsafe_allow_html=True)

nama_list = df_anggota["Nama"].tolist() if not df_anggota.empty and "Nama" in df_anggota.columns else []
kta_map = {}
if not df_anggota.empty and "No KTA" in df_anggota.columns and "Nama" in df_anggota.columns:
    kta_map = dict(zip(df_anggota["Nama"], df_anggota["No KTA"]))

with st.form("form_iuran", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        pilih_nama = st.selectbox(
            "Pilih Anggota *",
            options=[""] + nama_list,
            format_func=lambda x: "-- Pilih Anggota --" if x == "" else x
        )
    with col2:
        thn_dari = st.number_input("Tahun Dari *", min_value=2000, max_value=2100, value=2024, step=1)
    with col3:
        thn_sampai = st.number_input("Tahun Sampai *", min_value=2000, max_value=2100, value=2024, step=1)
    with col4:
        status_iur = st.selectbox("Status *", ["Lunas", "Belum Lunas"])

    simpan = st.form_submit_button("💾 Simpan Status Iuran", use_container_width=True)

if simpan:
    if not pilih_nama:
        st.error("Pilih anggota terlebih dahulu.")
    elif thn_sampai < thn_dari:
        st.error("Tahun sampai tidak boleh lebih kecil dari tahun dari.")
    else:
        no_kta_sel = str(kta_map.get(pilih_nama, ""))
        ok = simpan_iuran({
            "no_kta": no_kta_sel,
            "nama": pilih_nama,
            "tahun_dari": thn_dari,
            "tahun_sampai": thn_sampai,
            "status_iuran": status_iur
        })
        if ok:
            st.success(f"✅ Iuran **{pilih_nama}** ({thn_dari}–{thn_sampai}) disimpan sebagai **{status_iur}**!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("❌ Gagal menyimpan.")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2 = st.tabs(["💳  Data Iuran", "👥  Data Anggota"])

with tab1:
    col_r, _ = st.columns([1, 5])
    with col_r:
        if st.button("🔄 Refresh", key="ref_iuran"):
            st.cache_data.clear()
            st.rerun()

    if df_iuran.empty:
        st.info("Belum ada data iuran.")
    else:
        st.dataframe(df_iuran, use_container_width=True, hide_index=True, height=350)
        st.caption(f"Total {len(df_iuran)} data iuran")

        st.markdown("---")
        st.markdown("**🗑️ Hapus Data Iuran**")
        kta_iuran_list = df_iuran["No KTA"].astype(str).tolist() if "No KTA" in df_iuran.columns else []
        col_del1, col_del2 = st.columns([3, 1])
        with col_del1:
            del_iuran = st.selectbox("Pilih No. KTA untuk dihapus", [""] + kta_iuran_list, key="del_iuran")
        with col_del2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Hapus", use_container_width=True, type="primary", key="hapus_iuran_btn"):
                if del_iuran:
                    if hapus_iuran(del_iuran):
                        st.success(f"Data iuran No. KTA {del_iuran} dihapus.")
                        st.cache_data.clear()
                        st.rerun()

with tab2:
    col_r2, _ = st.columns([1, 5])
    with col_r2:
        if st.button("🔄 Refresh", key="ref_anggota"):
            st.cache_data.clear()
            st.rerun()

    if df_anggota.empty:
        st.info("Belum ada data anggota.")
    else:
        cols_show = ["Nama", "Jenis Kelamin", "No HP", "Nomor STR", "No KTA",
                     "Status Pekerjaan", "Instansi", "Gaji", "Status Keanggotaan"]
        cols_show = [c for c in cols_show if c in df_anggota.columns]
        st.dataframe(df_anggota[cols_show], use_container_width=True, hide_index=True, height=400)
        st.caption(f"Total {len(df_anggota)} anggota terdaftar")

        st.markdown("---")
        st.markdown("**🗑️ Hapus Data Anggota**")
        kta_list = df_anggota["No KTA"].astype(str).tolist() if "No KTA" in df_anggota.columns else []

        def fmt_kta(x):
            if x == "":
                return "-- Pilih --"
            match = df_anggota[df_anggota["No KTA"].astype(str) == x]
            nama = match["Nama"].values[0] if len(match) > 0 else ""
            return f"{x} – {nama}"

        col_da1, col_da2 = st.columns([3, 1])
        with col_da1:
            del_anggota = st.selectbox("Pilih No. KTA anggota", [""] + kta_list,
                                       key="del_anggota", format_func=fmt_kta)
        with col_da2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Hapus", use_container_width=True, type="primary", key="hapus_anggota_btn"):
                if del_anggota:
                    if hapus_anggota(del_anggota):
                        st.success(f"Anggota No. KTA {del_anggota} dihapus.")
                        st.cache_data.clear()
                        st.rerun()
