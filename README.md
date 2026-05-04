# Aplikasi Dashboard Status Iuran DPC

Aplikasi ini menggunakan **Streamlit** untuk antarmuka pengguna dan **Google Sheets** sebagai basis data.

## Cara Menjalankan Secara Lokal

1. **Install Python:** Pastikan Anda sudah menginstal Python di komputer Anda.
2. **Install Dependencies:** Buka terminal/command prompt di folder aplikasi ini, lalu jalankan:
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Kredensial (Google Sheets):**
   - Buka file `.streamlit/secrets.toml`.
   - Masukkan `password` untuk login admin.
   - Masukkan kredensial dari Service Account Google Cloud Anda (lihat panduan di bawah).
   - Masukkan URL Google Sheets Anda di bagian `spreadsheet`.
4. **Jalankan Aplikasi:**
   ```bash
   streamlit run app.py
   ```

## Panduan Setup Google Sheets API

Agar aplikasi bisa membaca dan menulis data secara permanen, kita menggunakan Google Sheets. Berikut langkah-langkahnya:

1. Buat file **Google Sheets** baru.
2. Buat Header Kolom di baris pertama: `ID`, `Nama`, `Lunas_Tahun`, `Tidak_Lunas_Tahun`. Biarkan sisanya kosong.
3. Buka [Google Cloud Console](https://console.cloud.google.com/).
4. Buat **Project** baru.
5. Pergi ke **APIs & Services > Library**, lalu cari dan aktifkan:
   - **Google Sheets API**
   - **Google Drive API**
6. Pergi ke **APIs & Services > Credentials**.
7. Klik **Create Credentials > Service Account**. Beri nama (misal: `streamlit-db`).
8. Setelah terbuat, klik Service Account tersebut, buka tab **Keys**, lalu **Add Key > Create new key**. Pilih format **JSON** dan unduh filenya.
9. Buka file JSON yang terunduh menggunakan Notepad/teks editor.
10. Salin isi data dari file JSON tersebut (seperti `project_id`, `private_key`, `client_email`) ke dalam file `.streamlit/secrets.toml`.
    - *Penting: Perhatikan format `private_key` agar tetap menjaga baris baru (`\n`).*
11. Buka file Google Sheets Anda, klik tombol **Share** (Bagikan) di pojok kanan atas, lalu tambahkan email *Service Account* Anda (yang berakhiran `@...iam.gserviceaccount.com`) dan beri akses sebagai **Editor**.

## Panduan Deploy ke Streamlit Community Cloud (Gratis)

1. Buat akun di [GitHub](https://github.com/) dan [Streamlit Community Cloud](https://share.streamlit.io/).
2. Hubungkan akun GitHub Anda ke Streamlit.
3. Buat repositori baru di GitHub (misalnya: `dashboard-iuran-dpc`).
4. Upload 3 file ini ke repositori GitHub tersebut:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   > **JANGAN UPLOAD folder `.streamlit` atau file `secrets.toml` ke GitHub!**
5. Di Streamlit Cloud, klik **New App**.
6. Pilih repositori GitHub Anda, branch `main`, dan main file path `app.py`.
7. **PENTING:** Sebelum klik Deploy, klik tulisan **Advanced settings...**
8. Di bagian **Secrets**, salin semua isi dari file `.streamlit/secrets.toml` Anda di komputer lokal dan paste ke dalam kotak teks Secrets di Streamlit Cloud.
9. Klik **Deploy**! Aplikasi Anda sekarang sudah *live* dan dapat diakses publik.
