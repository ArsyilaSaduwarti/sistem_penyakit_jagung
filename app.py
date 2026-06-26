import streamlit as st
from database.koneksi import get_connection

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="SistemPakar Jagung",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS / Design System ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght=300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

/* ── App Background ── */
.stApp {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 30%, #f0f9ff 70%, #fefce8 100%) !important;
    min-height: 100vh;
}

/* ══════════════════════════════════════════════
   GLOBAL TEXT — semua teks utama harus gelap
   ══════════════════════════════════════════════ */
.stApp, .stApp p, .stApp span, .stApp div,
.stApp label, .stApp li, .stApp td, .stApp th {
    color: #1e293b !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: #1e293b !important;
}

/* ══════════════════════════════════════════════
   SIDEBAR
   ══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #15803d 0%, #166534 60%, #14532d 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
    width: 100% !important;
    margin-top: 8px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.25) !important;
    transform: translateX(4px) !important;
}
/* Nav links sidebar */
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span,
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p {
    color: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* ── Main Content Area ── */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1200px !important;
}

/* ══════════════════════════════════════════════
   METRIC CARDS
   ══════════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(21, 128, 61, 0.08), 0 1px 3px rgba(0,0,0,0.05) !important;
    border: 1px solid #dcfce7 !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] * {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: #475569 !important;
    font-size: 0.85rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] * {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 800 !important;
    color: #15803d !important;
    font-size: 2rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"],
[data-testid="metric-container"] [data-testid="stMetricDelta"] * {
    color: #64748b !important;
    font-size: 0.8rem !important;
}

/* ══════════════════════════════════════════════
   BUTTONS
   ══════════════════════════════════════════════ */
.stButton > button {
    font-family: 'Poppins', sans-serif !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: #f1f5f9 !important;
    color: #334155 !important;
    border: 1.5px solid #cbd5e1 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #e2e8f0 !important;
    color: #1e293b !important;
}

/* ══════════════════════════════════════════════
   TEXT INPUT
   ══════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border-radius: 10px !important;
    font-family: 'Poppins', sans-serif !important;
    border: 1.5px solid #cbd5e1 !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #94a3b8 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.12) !important;
}
/* Input label */
.stTextInput label p,
.stTextArea label p,
.stSelectbox label p,
.stRadio label p,
.stCheckbox label p {
    color: #334155 !important;
    font-weight: 500 !important;
    font-family: 'Poppins', sans-serif !important;
}

/* ══════════════════════════════════════════════
   SELECTBOX / DROPDOWN
   ══════════════════════════════════════════════ */
/* Container selectbox */
.stSelectbox > div > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}
/* Box utama yang terlihat */
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
/* Teks yang tampil di dalam box */
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] input {
    color: #1e293b !important;
    background-color: transparent !important;
    font-family: 'Poppins', sans-serif !important;
}
/* Dropdown list (popup) */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
/* Item di dalam list dropdown */
li[role="option"],
[data-baseweb="menu"] li,
ul[role="listbox"] li {
    background-color: #ffffff !important;
    color: #1e293b !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.9rem !important;
}
/* Hover item */
li[role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background-color: #f0fdf4 !important;
    color: #15803d !important;
}
/* Item terpilih (selected) */
li[role="option"][aria-selected="true"] {
    background-color: #dcfce7 !important;
    color: #15803d !important;
    font-weight: 600 !important;
}
/* Ikon panah dropdown */
.stSelectbox [data-baseweb="select"] svg {
    fill: #64748b !important;
}

/* ══════════════════════════════════════════════
   RADIO BUTTON
   ══════════════════════════════════════════════ */
.stRadio > div {
    background: #f8fafc !important;
    border-radius: 12px !important;
    padding: 0.3rem !important;
    border: 1.5px solid #e2e8f0 !important;
    gap: 0.3rem !important;
}
.stRadio label {
    color: #475569 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s !important;
}
.stRadio label[data-selected="true"],
.stRadio label:has(input:checked) {
    background: #15803d !important;
    color: #ffffff !important;
}
/* Teks di dalam radio label */
.stRadio label p,
.stRadio label span {
    color: inherit !important;
}

/* ══════════════════════════════════════════════
   CHECKBOX
   ══════════════════════════════════════════════ */
.stCheckbox label {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: #334155 !important;
}
.stCheckbox label p,
.stCheckbox label span {
    color: #334155 !important;
}

/* ══════════════════════════════════════════════
   TABS
   ══════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #1e293b !important;
    background: rgba(255,255,255,0.6) !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #15803d !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: inherit !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1rem !important;
}

/* ── Alert / Info / Success / Warning boxes ── */
.stAlert {
    border-radius: 14px !important;
    font-family: 'Poppins', sans-serif !important;
    border-left-width: 4px !important;
}
.stAlert p { color: inherit !important; }

/* ── DataFrames ── */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader,
details summary {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    background: #f0fdf4 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
}
.streamlit-expanderContent *,
details[open] > div * {
    color: #334155 !important;
}

/* ── Divider ── */
hr { border-color: #dcfce7 !important; }

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 10px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    background: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
}
.stDownloadButton > button:hover {
    background: #0284c7 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'user_nama' not in st.session_state:
    st.session_state['user_nama'] = ""
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "user"


# ─── AUTH PAGE ─────────────────────────────────────────────
def halaman_auth():
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 1rem 1.5rem;">
        <div style="font-size:4rem; margin-bottom:0.5rem;">🌽</div>
        <h1 style="font-size:2.2rem; background: linear-gradient(135deg, #15803d, #22c55e);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text; margin-bottom:0.4rem;">
            Sistem Pakar Penyakit Jagung
        </h1>
        <p style="color:#64748b; font-size:1rem; font-family:'Poppins',sans-serif; font-weight:400;">
            Diagnosis cerdas berbasis <strong>Certainty Factor</strong> — cepat, akurat, tepercaya
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1.4, 1])
    with col_center:
        st.markdown("""
        <div style="background:white; border-radius:20px;
                    box-shadow:0 8px 30px rgba(21,128,61,0.12);
                    padding:2rem; border:1px solid #dcfce7;">
        """, unsafe_allow_html=True)

        menu_auth = st.radio("", ["🔑 Login", "📝 Register"], horizontal=True, label_visibility="collapsed")

        if "Login" in menu_auth:
            st.markdown("<h3 style='color:#15803d; margin-bottom:1rem;'>Masuk ke Akun</h3>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="contoh@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")

            if st.button("🚀 Log In", type="primary", use_container_width=True):
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id_user']
                    st.session_state['user_nama'] = user['nama']
                    st.session_state['user_role'] = user.get('role', 'user')
                    st.success(f"Selamat datang, **{user['nama']}**! ✨")
                    st.rerun()
                else:
                    st.error("Email atau password tidak sesuai.")

        else:
            st.markdown("<h3 style='color:#15803d; margin-bottom:1rem;'>Buat Akun Baru</h3>", unsafe_allow_html=True)
            nama_baru  = st.text_input("Nama Lengkap", placeholder="Nama Anda")
            email_baru = st.text_input("Email", placeholder="contoh@email.com", key="reg_email")
            pass_baru  = st.text_input("Password", type="password", placeholder="Min. 6 karakter", key="reg_pass")

            if st.button("✅ Daftar Sekarang", type="primary", use_container_width=True):
                if not all([nama_baru, email_baru, pass_baru]):
                    st.warning("Semua kolom wajib diisi.")
                else:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO users (nama, email, password, role) VALUES (%s, %s, %s, 'user')",
                            (nama_baru, email_baru, pass_baru)
                        )
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Akun berhasil dibuat! Silakan login.")
                    except Exception as e:
                        st.error(f"Gagal mendaftar: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:2rem; color:#94a3b8; font-size:0.8rem; font-family:'Poppins',sans-serif;">
        Referensi: Mahyuni &amp; Munar (2021) · JACIS Vol.6 (2026) · SQUARE Vol.6
    </div>
    """, unsafe_allow_html=True)


# ─── SIDEBAR for logged-in users ──────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:1.2rem 0.5rem 0.8rem; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom:1rem;">
            <div style="font-size:2rem; margin-bottom:0.3rem;">🌽</div>
            <div style="font-size:0.75rem; opacity:0.7; letter-spacing:0.1em; text-transform:uppercase;">Sistem Pakar</div>
            <div style="font-size:1.1rem; font-weight:700;">Penyakit Jagung</div>
        </div>
        <div style="background:rgba(255,255,255,0.12); border-radius:12px; padding:0.8rem 1rem; margin-bottom:1rem;">
            <div style="font-size:0.72rem; opacity:0.7;">Pengguna aktif (${st.session_state['user_role'].upper()})</div>
            <div style="font-weight:600; font-size:0.95rem;">👋 {st.session_state['user_nama']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Log Out", type="secondary"):
            for key in ['logged_in', 'user_id', 'user_nama', 'user_role']:
                st.session_state[key] = False if key == 'logged_in' else (None if key in ['user_id'] else "user")
            st.rerun()


# ─── MAIN NAVIGATION ──────────────────────────────────────
if not st.session_state['logged_in']:
    st.navigation([st.Page(halaman_auth, title="Autentikasi", icon="🔒")]).run()
else:
    render_sidebar()
    
    # Menu Dasar Pengguna (User/Petani)
    pages = {
        "Menu Utama": [
            st.Page("pages/dashboard.py",      title="Dashboard",        icon="📊", default=True),
            st.Page("pages/diagnosa.py",        title="Mulai Diagnosa",   icon="🩺"),
        ],
        "Basis Pengetahuan": [
            st.Page("pages/knowledge_base.py", title="Knowledge Base",   icon="📚"),
            st.Page("pages/riwayat.py",        title="Riwayat Diagnosa", icon="📜"),
        ],
    }
    
    # Kondisi Tambahan: Menu khusus Admin
    if st.session_state['user_role'] == 'admin':
        pages["Panel Administrator"] = [
            st.Page("pages/admin_kelola.py",  title="Kelola Data Master", icon="⚙️")
        ]
        
    st.navigation(pages).run()