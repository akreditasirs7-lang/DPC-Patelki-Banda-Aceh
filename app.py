import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi halaman Streamlit agar lebih luas
st.set_page_config(page_title="Lab Staff Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Menyembunyikan elemen bawaan Streamlit (header, footer, padding)
hide_streamlit_style = """
<style>
    /* Menghapus padding utama */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    /* Menyembunyikan header Streamlit */
    header {visibility: hidden;}
    /* Menyembunyikan footer Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Membuat iframe memenuhi layar */
    iframe {
        width: 100%;
        height: 100vh;
        border: none;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Membaca file HTML, CSS, dan JS
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    with open("styles.css", "r", encoding="utf-8") as f:
        css_content = f.read()

    with open("script.js", "r", encoding="utf-8") as f:
        js_content = f.read()

    # Menggabungkan kembali (inline) file CSS dan JS ke dalam HTML
    # Mengganti tag link CSS
    html_content = html_content.replace(
        '<link rel="stylesheet" href="styles.css">', 
        f"<style>{css_content}</style>"
    )

    # Mengganti tag script eksternal menjadi inline script
    html_content = html_content.replace(
        '<script src="script.js"></script>', 
        f"<script>{js_content}</script>"
    )

    # Menampilkan HTML di aplikasi Streamlit
    components.html(html_content, height=1200, scrolling=True)

except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file: {e}")
