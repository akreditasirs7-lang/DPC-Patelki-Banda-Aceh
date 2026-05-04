import streamlit as st
import hmac


def check_password() -> bool:
    """Returns True jika admin sudah login."""
    if st.session_state.get("authenticated"):
        return True
    return False


def login_form():
    """Tampilkan form login admin."""
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center;margin-bottom:1.5rem'>
            <div style='width:64px;height:64px;border-radius:50%;
                background:linear-gradient(135deg,#3B82F6,#1D4ED8);
                display:flex;align-items:center;justify-content:center;
                font-size:26px;font-weight:700;color:white;
                margin:0 auto 12px;border:2px solid rgba(255,255,255,.2)'>P</div>
            <h2 style='color:#F1F5F9;font-size:20px;margin:0'>Login Admin</h2>
            <p style='color:#64748B;font-size:13px;margin-top:4px'>DPC Patelki Banda Aceh</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("🔐 Masuk", use_container_width=True)

            if submitted:
                ok_user = hmac.compare_digest(username, st.secrets["admin"]["username"])
                ok_pass = hmac.compare_digest(password, st.secrets["admin"]["password"])
                if ok_user and ok_pass:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

        st.markdown("""
        <div style='background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
            border-radius:8px;padding:12px 14px;font-size:12px;color:#93C5FD;
            margin-top:12px;line-height:1.7'>
            <b>Default:</b> admin / patelki2024<br>
            <span style='color:#475569'>Ganti di Streamlit Secrets setelah deploy.</span>
        </div>
        """, unsafe_allow_html=True)


def logout():
    st.session_state["authenticated"] = False
    st.rerun()
