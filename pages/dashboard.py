import streamlit as st
from database.koneksi import get_connection

# ── Stats from DB ──────────────────────────────────────────
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM gejala")
    total_gejala = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM penyakit")
    total_penyakit = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM rules_cf")
    total_rules = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM diagnosa WHERE id_user = %s", (st.session_state['user_id'],))
    total_diagnosa_saya = cursor.fetchone()[0]
    cursor.close()
    conn.close()
except:
    total_gejala = total_penyakit = total_rules = total_diagnosa_saya = 0

# ── CSS khusus dashboard ───────────────────────────────────
st.markdown("""
<style>
/* Pastikan semua kolom punya tinggi sama (equal height) */
[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}
[data-testid="stHorizontalBlock"] > div {
    display: flex !important;
    flex-direction: column !important;
}
/* Metric delta teks tidak hilang */
[data-testid="stMetricDelta"] svg { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;">
    <h1 style="font-size:2rem; font-weight:800; color:#1e293b; margin-bottom:0.3rem;">
        📊 Dashboard
    </h1>
    <p style="color:#64748b; font-size:0.95rem; font-family:'Poppins',sans-serif; margin:0;">
        Selamat datang kembali, <strong style="color:#15803d;">{st.session_state['user_nama']}</strong>!
        Sistem siap membantu diagnosis penyakit tanaman jagung Anda.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Metric Cards ───────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌿 Total Gejala",   f"{total_gejala}",        "Dalam database")
with col2:
    st.metric("🦠 Jenis Penyakit", f"{total_penyakit}",      "Terdaftar")
with col3:
    st.metric("📋 Aturan CF",      f"{total_rules}",         "Rules aktif")
with col4:
    st.metric("🩺 Diagnosa Saya",  f"{total_diagnosa_saya}", "Riwayat saya")

st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

# ── Penyakit Cards ─────────────────────────────────────────
st.markdown("""
<h3 style="font-size:1.15rem; font-weight:700; color:#1e293b;
           margin-bottom:1rem;">🦠 Penyakit yang Dapat Didiagnosis</h3>
""", unsafe_allow_html=True)

penyakit_info = [
    ("🍃", "Hawar Daun",    "#22c55e", "#f0fdf4", "#dcfce7", "Bercak memanjang hijau keabu-abuan pada daun jagung"),
    ("🟫", "Busuk Pelepah", "#f59e0b", "#fffbeb", "#fde68a", "Bercak kemerahan atau keabuan pada pelepah daun"),
    ("🌱", "Bulai",         "#14b8a6", "#f0fdfa", "#99f6e4", "Klorosis putih kekuningan memanjang pada daun muda"),
    ("🌽", "Busuk Tongkol", "#ef4444", "#fef2f2", "#fecaca", "Perubahan warna dan pembusukan biji pada tongkol"),
    ("🪵", "Busuk Batang",  "#8b5cf6", "#faf5ff", "#ddd6fe", "Pembusukan pada pangkal dan bagian dalam batang"),
    ("🟠", "Karat Daun",    "#f97316", "#fff7ed", "#fed7aa", "Pustul coklat kemerahan pada permukaan daun"),
]

# Render 2 baris × 3 kolom, tiap card full-height flex
row1 = penyakit_info[:3]
row2 = penyakit_info[3:]

for row in [row1, row2]:
    cols = st.columns(3)
    for col, (icon, nama, color, bg, border_color, deskripsi) in zip(cols, row):
        with col:
            st.markdown(f"""
            <div style="
                background:{bg};
                border:1.5px solid {border_color};
                border-radius:16px;
                padding:1.2rem 1.3rem;
                height:100%;
                min-height:160px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                box-sizing:border-box;
                margin-bottom:1rem;
            ">
                <div>
                    <div style="font-size:1.8rem; margin-bottom:0.5rem; line-height:1;">{icon}</div>
                    <div style="
                        font-weight:700;
                        color:#1e293b;
                        font-family:'Poppins',sans-serif;
                        font-size:0.95rem;
                        margin-bottom:0.4rem;
                        line-height:1.3;
                    ">{nama}</div>
                    <div style="
                        color:#475569;
                        font-size:0.8rem;
                        font-family:'Poppins',sans-serif;
                        line-height:1.5;
                    ">{deskripsi}</div>
                </div>
                <div style="margin-top:0.8rem;">
                    <span style="
                        background:{color};
                        color:white;
                        border-radius:20px;
                        padding:0.2rem 0.8rem;
                        font-size:0.72rem;
                        font-family:'Poppins',sans-serif;
                        font-weight:600;
                        display:inline-block;
                    ">Terdeteksi CF</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

# ── How to Use ────────────────────────────────────────────
st.markdown("""
<h3 style="font-size:1.15rem; font-weight:700; color:#1e293b; margin-bottom:1rem;">
    💡 Cara Menggunakan Sistem
</h3>
""", unsafe_allow_html=True)

steps = [
    ("#22c55e", "1", "Buka menu <strong>Mulai Diagnosa</strong> di sidebar kiri"),
    ("#f59e0b", "2", "Centang gejala-gejala yang tampak pada tanaman jagung Anda"),
    ("#14b8a6", "3", "Pilih tingkat keyakinan untuk setiap gejala yang dipilih"),
    ("#8b5cf6", "4", "Klik <strong>Hitung Diagnosis</strong> — sistem menghitung nilai Certainty Factor"),
]

steps_html = ""
for color, num, text in steps:
    steps_html += f"""
    <div style="display:flex; align-items:center; gap:1rem; padding:0.6rem 0;">
        <div style="
            background:{color};
            color:white;
            border-radius:50%;
            width:34px; height:34px;
            min-width:34px;
            display:flex; align-items:center; justify-content:center;
            font-weight:700; font-family:'Poppins',sans-serif;
            font-size:0.85rem;
        ">{num}</div>
        <span style="font-family:'Poppins',sans-serif; color:#334155; font-size:0.9rem; line-height:1.5;">
            {text}
        </span>
    </div>
    """

st.markdown(f"""
<div style="
    background:white;
    border-radius:16px;
    padding:1.4rem 1.8rem;
    box-shadow:0 2px 12px rgba(21,128,61,0.07);
    border:1px solid #dcfce7;
">
    {steps_html}
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;
    color:#94a3b8;
    font-size:0.78rem;
    font-family:'Poppins',sans-serif;
    padding:1rem;
    border-top:1px solid #e2e8f0;
">
    📖 Referensi: Mahyuni &amp; Munar (2021) &nbsp;·&nbsp;
    JACIS Vol.6 No.1 (2026), Widyassari &amp; Puspita &nbsp;·&nbsp;
    SQUARE Journal of Mathematics Education Vol.6
</div>
""", unsafe_allow_html=True)
