import streamlit as st
import pandas as pd
from database.koneksi import get_connection

# ── Header ────────────────────────────────────────────────
st.markdown("""
<h1 style="margin-bottom:0.3rem;">📜 Riwayat Diagnosa</h1>
<p style="color:#64748b; font-family:'Poppins',sans-serif; margin-bottom:1.5rem;">
    Daftar seluruh riwayat konsultasi diagnosis penyakit tanaman jagung Anda.
</p>
""", unsafe_allow_html=True)

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute(
    """SELECT tanggal, hasil_penyakit, nilai_cf
       FROM diagnosa
       WHERE id_user = %s
       ORDER BY tanggal DESC""",
    (st.session_state['user_id'],)
)
data_riwayat = cursor.fetchall()
cursor.close()
conn.close()

if data_riwayat:
    df = pd.DataFrame(data_riwayat)
    df.columns = ["Tanggal", "Hasil Penyakit", "Nilai CF (%)"]

    # Summary stats
    total = len(df)
    avg_cf = df["Nilai CF (%)"].astype(float).mean()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📋 Total Diagnosa", f"{total} kali")
    with col2:
        st.metric("📊 Rata-rata CF", f"{avg_cf:.1f}%")

    st.write("")

    # Color rows by CF
    def color_row(val):
        try:
            v = float(val)
            if v > 70:
                return "background-color: #f0fdf4; color: #15803d; font-weight: 600;"
            elif v > 40:
                return "background-color: #f0f9ff; color: #0369a1;"
            else:
                return "background-color: #fffbeb; color: #92400e;"
        except:
            return ""

    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.2rem 1.5rem;
                box-shadow:0 2px 10px rgba(21,128,61,0.07); border:1px solid #dcfce7; margin-bottom:1rem;">
        <div style="font-weight:600; color:#15803d; font-family:'Poppins',sans-serif; margin-bottom:0.3rem;">
            🟢 CF &gt; 70% = Tinggi &nbsp; 🔵 CF 40–70% = Sedang &nbsp; 🟡 CF &lt; 40% = Rendah
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df.style.applymap(color_row, subset=["Nilai CF (%)"]),
        use_container_width=True,
        hide_index=True
    )

else:
    st.markdown("""
    <div style="background:white; border-radius:16px; padding:2.5rem; text-align:center;
                box-shadow:0 2px 12px rgba(21,128,61,0.07); border:1px solid #dcfce7;">
        <div style="font-size:3rem; margin-bottom:0.8rem;">🌱</div>
        <div style="font-weight:700; color:#334155; font-family:'Poppins',sans-serif;
                    font-size:1.1rem; margin-bottom:0.4rem;">Belum Ada Riwayat</div>
        <div style="color:#94a3b8; font-family:'Poppins',sans-serif; font-size:0.88rem;">
            Anda belum pernah melakukan diagnosa. Mulai dari menu <strong>Mulai Diagnosa</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)