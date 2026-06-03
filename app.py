import streamlit as st
from database.koneksi import get_connection
import hashlib

st.set_page_config(page_title="Sistem Pakar Jagung", page_icon="🌽", layout="wide")

# Menggunakan enkripsi MD5/SHA256 sesuai kebutuhan. Di sini kita pakai SHA256 agar aman.
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'user_nama' not in st.session_state:
    st.session_state['user_nama'] = ""

def halaman_auth():
    st.title("🌽 Aplikasi Sistem Pakar Penyakit Jagung")
    menu_auth = st.radio("Silakan Pilih Aksi:", ["Login", "Register"], horizontal=True)

    if menu_auth == "Login":
        st.subheader("🔑 Masuk ke Akun Anda")
        email = st.text_input("Email (Sesuai Database)")
        password = st.text_input("Password", type="password")
        
        if st.button("Log In", type="primary"):
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # COCOK: Menggunakan kolom email dan password dari tabel users
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password)) # Jika di DB passwordnya plain text
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user['id_user'] 
                st.session_state['user_nama'] = user['nama']
                st.success(f"Selamat datang, {user['nama']}! Berhasil login.")
                st.rerun()
            else:
                st.error("Email atau password salah!")

    elif menu_auth == "Register":
        st.subheader("📝 Buat Akun Baru")
        nama_baru = st.text_input("Nama Lengkap")
        email_baru = st.text_input("Email")
        pass_baru = st.text_input("Password Baru", type="password")

        if st.button("Daftar Akun"):
            if nama_baru == "" or email_baru == "" or pass_baru == "":
                st.warning("Semua data wajib diisi!")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    # COCOK: Melakukan insert sesuai kolom asli tabel users
                    cursor.execute(
                        "INSERT INTO users (nama, email, password, role) VALUES (%s, %s, %s, 'user')", 
                        (nama_baru, email_baru, pass_baru)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    st.success("Akun berhasil dibuat! Silakan masuk ke menu Login.")
                except Exception as e:
                    st.error(f"Gagal Register. Error: {e}")

# --- KONTROL NAVIGASI UTAMA ---
if not st.session_state['logged_in']:
    halaman_aktif = st.navigation([st.Page(halaman_auth, title="Autentikasi", icon="🔒")])
    halaman_aktif.run()
else:
    def tombol_logout():
        st.sidebar.title(f"👋 Halo, {st.session_state['user_nama']}!")
        if st.sidebar.button("🚪 Log Out", type="secondary"):
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['user_nama'] = ""
            st.rerun()

    halaman_aktif = st.navigation({
        "Menu Utama": [
            st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True),
            st.Page("pages/diagnosa.py", title="Mulai Diagnosa", icon="🩺"),
        ],
        "Basis Pengetahuan": [
            st.Page("pages/knowledge_base.py", title="Knowledge Base", icon="📚"),
            st.Page("pages/riwayat.py", title="Riwayat Diagnosa", icon="📜"),
        ]
    })
    tombol_logout()
    halaman_aktif.run()