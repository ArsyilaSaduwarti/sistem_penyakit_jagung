import streamlit as st
from database.koneksi import get_connection

st.title("📊 Dashboard Utama")
st.subheader(f"Selamat Datang di Sistem Pakar Jagung, {st.session_state['user_nama']}!")

# Ambil statistik dari database
try:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM gejala")
    total_gejala = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM penyakit")
    total_penyakit = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
except:
    total_gejala, total_penyakit = 0, 0

# Tampilkan Ringkasan Berbentuk Kartu (Metrics)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Gejala di Sistem", value=f"{total_gejala} Gejala")
with col2:
    st.metric(label="Total Penyakit Terdaftar", value=f"{total_penyakit} Jenis")

st.write("---")
st.info("""
**💡 Petunjuk Penggunaan:**
1. Masuk ke menu **Mulai Diagnosa** di sidebar kiri.
2. Centang gejala-gejala yang tampak pada tanaman jagung Anda.
3. Gunakan panduan gambar yang tertera di samping gejala jika Anda ragu.
4. Tentukan tingkat keyakinan Anda, lalu klik **Hitung Diagnosis Penyakit**.
""")