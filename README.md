# 🔬 Sistem Data Anggota DPC Patelki Banda Aceh

Aplikasi web manajemen anggota berbasis **Streamlit + Google Sheets** dengan animasi sel darah & laboratorium.

---

## 📁 Struktur Project

```
patelki/
├── app.py                  ← Halaman publik (dashboard)
├── pages/
│   └── admin.py            ← Halaman admin (butuh login)
├── utils/
│   ├── sheets.py           ← Koneksi Google Sheets
│   ├── auth.py             ← Sistem login
│   └── style.py            ← CSS + animasi
├── .streamlit/
│   ├── config.toml         ← Tema dark
│   └── secrets.toml        ← Kredensial (JANGAN di-commit!)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Cara Deploy ke Streamlit Cloud

### STEP 1 — Siapkan Google Sheets & Service Account

1. Buka [console.cloud.google.com](https://console.cloud.google.com)
2. Buat **New Project** → beri nama misal `patelki-app`
3. Di search bar, aktifkan **Google Sheets API** dan **Google Drive API**
4. Klik **Credentials** → **Create Credentials** → **Service Account**
   - Nama: `patelki-sheets`
   - Klik **Create and Continue** → **Done**
5. Klik service account yang baru dibuat → tab **Keys** → **Add Key** → **JSON**
   - File JSON akan terdownload otomatis → **simpan baik-baik!**
6. Buka Google Sheets kamu → klik **Share** → paste email service account (dari file JSON, field `client_email`) → beri akses **Editor**
7. Copy **Spreadsheet ID** dari URL Sheets kamu:
   `https://docs.google.com/spreadsheets/d/**SPREADSHEET_ID**/edit`

---

### STEP 2 — Push ke GitHub

```bash
# Di terminal / Git Bash
cd patelki
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Buat repo baru di github.com, lalu:
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

> ⚠️ Pastikan `.streamlit/secrets.toml` TIDAK ikut ter-push (sudah ada di `.gitignore`)

---

### STEP 3 — Deploy di Streamlit Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan GitHub
3. Klik **New app**
4. Pilih repo yang baru di-push → Main file: `app.py` → **Deploy**
5. Setelah deploy, klik **⚙ Settings** → **Secrets**
6. Paste isi berikut (isi dari file JSON service account):

```toml
[admin]
username = "admin"
password = "GANTI_PASSWORD_BARU"

[gcp_service_account]
type = "service_account"
project_id = "ISI_DARI_JSON"
private_key_id = "ISI_DARI_JSON"
private_key = "-----BEGIN RSA PRIVATE KEY-----\nISI_DARI_JSON\n-----END RSA PRIVATE KEY-----\n"
client_email = "ISI_DARI_JSON"
client_id = "ISI_DARI_JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "ISI_DARI_JSON"

[sheets]
spreadsheet_id = "SPREADSHEET_ID_KAMU"
```

7. Klik **Save** → app akan restart otomatis

---

### STEP 4 — Ganti Password Admin

Di bagian **Secrets** Streamlit Cloud, ubah:
```toml
[admin]
username = "admin_patelki"     ← ganti sesuai keinginan
password = "password_rahasia"  ← ganti dengan password kuat
```

---

## 🖥️ Cara Akses

| Halaman | URL |
|---------|-----|
| Dashboard Publik | `https://app-kamu.streamlit.app` |
| Panel Admin | `https://app-kamu.streamlit.app/admin` |

---

## 🔐 Login Admin

- Buka URL `/admin`
- Masukkan username & password sesuai Secrets
- Default: `admin` / `patelki2024` ← **segera ganti setelah deploy!**

---

## 🛠️ Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buat file `.streamlit/secrets.toml` dari template yang ada, isi dengan kredensial asli.
