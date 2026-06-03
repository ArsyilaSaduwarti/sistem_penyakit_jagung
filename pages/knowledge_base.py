import streamlit as st
import pandas as pd
from database.koneksi import get_connection

# ── Header ────────────────────────────────────────────────
st.markdown("""
<h1 style="margin-bottom:0.3rem;">📚 Basis Pengetahuan (Knowledge Base)</h1>
<p style="color:#64748b; font-family:'Poppins',sans-serif; margin-bottom:1.5rem;">
    Data master penyakit, gejala, dan aturan Certainty Factor yang digunakan sistem.
    Disusun berdasarkan referensi pakar &amp; jurnal ilmiah terkini.
</p>
""", unsafe_allow_html=True)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# ── Tab Layout ────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🦠 Penyakit", "🌿 Gejala", "📋 Aturan CF"])

with tab1:
    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.2rem 1.5rem;
                box-shadow:0 2px 10px rgba(21,128,61,0.07); border:1px solid #dcfce7; margin-bottom:1rem;">
        <div style="font-weight:700; color:#15803d; font-family:'Poppins',sans-serif; margin-bottom:0.3rem;">
            🦠 Daftar Penyakit Tanaman Jagung
        </div>
        <div style="color:#64748b; font-size:0.85rem; font-family:'Poppins',sans-serif;">
            6 jenis penyakit dengan deskripsi lengkap dan solusi penanganan berdasarkan pakar &amp; jurnal JACIS 2026.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("SELECT kode_penyakit, nama_penyakit, deskripsi, solusi, referensi FROM penyakit")
    df_penyakit = pd.DataFrame(cursor.fetchall())
    df_penyakit.columns = ["Kode", "Nama Penyakit", "Deskripsi", "Solusi", "Referensi"]
    st.dataframe(df_penyakit, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.2rem 1.5rem;
                box-shadow:0 2px 10px rgba(21,128,61,0.07); border:1px solid #dcfce7; margin-bottom:1rem;">
        <div style="font-weight:700; color:#15803d; font-family:'Poppins',sans-serif; margin-bottom:0.3rem;">
            🌿 Daftar Gejala
        </div>
        <div style="color:#64748b; font-size:0.85rem; font-family:'Poppins',sans-serif;">
            30 gejala — diperluas dari 22 gejala awal menggunakan data dari jurnal JACIS 2026 &amp; SQUARE Vol.6.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("SELECT kode_gejala, nama_gejala FROM gejala ORDER BY id_gejala")
    df_gejala = pd.DataFrame(cursor.fetchall())
    df_gejala.columns = ["Kode Gejala", "Nama Gejala"]
    st.dataframe(df_gejala, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.2rem 1.5rem;
                box-shadow:0 2px 10px rgba(21,128,61,0.07); border:1px solid #dcfce7; margin-bottom:1rem;">
        <div style="font-weight:700; color:#15803d; font-family:'Poppins',sans-serif; margin-bottom:0.3rem;">
            📋 Aturan Certainty Factor (Rules)
        </div>
        <div style="color:#64748b; font-size:0.85rem; font-family:'Poppins',sans-serif;">
            Nilai CF Pakar (MB &amp; MD) untuk setiap pasangan penyakit–gejala.
            Nilai CF = MB − MD menunjukkan tingkat kepercayaan pakar.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("""
        SELECT r.id_rule, p.nama_penyakit, g.kode_gejala, g.nama_gejala,
               r.cf_pakar, r.mb, r.md
        FROM rules_cf r
        JOIN penyakit p ON r.id_penyakit = p.id_penyakit
        JOIN gejala g   ON r.id_gejala   = g.id_gejala
        ORDER BY r.id_penyakit, r.id_gejala
    """)
    df_rules = pd.DataFrame(cursor.fetchall())
    df_rules.columns = ["ID Rule", "Penyakit", "Kode Gejala", "Nama Gejala", "CF Pakar", "MB", "MD"]
    st.dataframe(df_rules, use_container_width=True, hide_index=True)

cursor.close()
conn.close()

# ── Referensi Box ─────────────────────────────────────────
st.write("")
st.markdown("""
<div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5); border-radius:14px;
            padding:1.2rem 1.5rem; border:1px solid #86efac;">
    <div style="font-weight:700; color:#15803d; font-family:'Poppins',sans-serif; margin-bottom:0.6rem;">
        📖 Referensi Ilmiah
    </div>
    <ul style="color:#334155; font-family:'Poppins',sans-serif; font-size:0.85rem;
               line-height:1.9; margin:0; padding-left:1.2rem;">
        <li>Mahyuni &amp; Munar (2021). Penerapan Sistem Pakar Metode Certainty Factor untuk Diagnosis Penyakit Tanaman Jagung.</li>
        <li>Widyassari, A.P. &amp; Puspita, U.F.D. (2026). Implementasi Metode Certainty Factor dan TOPSIS pada Diagnosis Penyakit Jagung.
            <em>JACIS Vol.6 No.1</em>, hal. 205–218. DOI: 10.47134/jacis.v6i1.181</li>
        <li>SQUARE: Journal of Mathematics and Mathematics Education, Vol. 6. Penerapan Sistem Pakar Menggunakan Metode Certainty Factor untuk Diagnosis Penyakit pada Tanaman Jagung.</li>
    </ul>
</div>
""", unsafe_allow_html=True)