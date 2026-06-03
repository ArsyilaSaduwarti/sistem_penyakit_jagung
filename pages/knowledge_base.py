import streamlit as st
import pandas as pd
from database.koneksi import get_connection

st.title("📚 Basis Pengetahuan Pakar (Knowledge Base)")
st.write("Daftar tabel master aturan, gejala, dan penyakit tanaman jagung langsung dari database.")

conn = get_connection()
cursor = conn.cursor(dictionary=True)

st.subheader("1. Tabel Penyakit")
cursor.execute("SELECT kode_penyakit, nama_penyakit, deskripsi, solusi FROM penyakit")
st.dataframe(pd.DataFrame(cursor.fetchall()), use_container_width=True)

st.subheader("2. Tabel Gejala")
cursor.execute("SELECT kode_gejala, nama_gejala FROM gejala")
st.dataframe(pd.DataFrame(cursor.fetchall()), use_container_width=True)

st.subheader("3. Aturan Keputusan (Rules CF)")
cursor.execute("""
    SELECT r.id_rule, p.nama_penyakit, g.nama_gejala, r.cf_pakar 
    FROM rules_cf r
    JOIN penyakit p ON r.id_penyakit = p.id_penyakit
    JOIN gejala g ON r.id_gejala = g.id_gejala
""")
st.dataframe(pd.DataFrame(cursor.fetchall()), use_container_width=True)

cursor.close()
conn.close()