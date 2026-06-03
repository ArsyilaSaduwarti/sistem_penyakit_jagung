import streamlit as st
import pandas as pd
from database.koneksi import get_connection

st.title("📜 Riwayat Hasil Diagnosa")
st.write("Berikut adalah daftar riwayat konsultasi diagnosa tanaman jagung Anda.")

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# COCOK: Mengambil riwayat berdasarkan id_user aktif
cursor.execute(
    "SELECT tanggal, hasil_penyakit, nilai_cf FROM diagnosa WHERE id_user = %s ORDER BY tanggal DESC",
    (st.session_state['user_id'],)
)
data_riwayat = cursor.fetchall()
cursor.close()
conn.close()

if data_riwayat:
    df_riwayat = pd.DataFrame(data_riwayat)
    st.dataframe(df_riwayat, use_container_width=True)
else:
    st.info("Anda belum pernah melakukan transaksi diagnosa.")