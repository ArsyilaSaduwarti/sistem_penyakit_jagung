import streamlit as st
from database.koneksi import get_connection
from datetime import datetime
import os

# ── Load Data ─────────────────────────────────────────────
conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM gejala ORDER BY id_gejala")
daftar_gejala = cursor.fetchall()
cursor.execute("SELECT * FROM penyakit")
rows_p = cursor.fetchall()
data_penyakit = {p['id_penyakit']: p for p in rows_p}
cursor.execute("SELECT id_penyakit, id_gejala, cf_pakar FROM rules_cf")
rules_cf = cursor.fetchall()
cursor.close()
conn.close()

# ── Inject Scoped CSS untuk Memperbaiki Warna Teks Gejala ──
# ── Inject Scoped CSS untuk Memperbaiki Warna Teks Gejala & Dropdown ──
st.markdown("""
<style>
    /* ── Checkbox label gelap & terbaca ── */
    .stCheckbox label,
    .stCheckbox label p,
    .stCheckbox label span {
        color: #1e293b !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* ── Selectbox / Dropdown: background putih, teks gelap ── */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] input,
    .stSelectbox [data-baseweb="select"] * {
        color: #1e293b !important;
        background-color: transparent !important;
    }

    /* ── Dropdown popup list ── */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
    }
    li[role="option"],
    ul[role="listbox"] li,
    [data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-family: 'Poppins', sans-serif !important;
    }
    li[role="option"]:hover {
        background-color: #f0fdf4 !important;
        color: #15803d !important;
    }
    li[role="option"][aria-selected="true"] {
        background-color: #dcfce7 !important;
        color: #15803d !important;
        font-weight: 600 !important;
    }

    /* ── Selectbox label ── */
    .stSelectbox label p {
        color: #334155 !important;
        font-weight: 500 !important;
    }

    /* ── Expander content ── */
    .streamlit-expanderContent *,
    details[open] > div * {
        color: #334155 !important;
    }
    
    /* ── Semua teks di area utama ── */
    .block-container p,
    .block-container span,
    .block-container div,
    .block-container label {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<h1 style="margin-bottom:0.3rem; color:#1e293b;">🩺 Form Diagnosis Penyakit Jagung</h1>
<p style="color:#64748b; font-family:'Poppins',sans-serif; margin-bottom:1.5rem;">
    Centang gejala yang tampak pada tanaman Anda, lalu tentukan tingkat keyakinan untuk setiap gejala.
</p>
""", unsafe_allow_html=True)

# ── CF Level Options ──────────────────────────────────────
opsi_keyakinan = {
    "— Pilih tingkat keyakinan —": -1,
    "Tidak Tahu (0.0)":           0.0,
    "Sedikit Yakin (0.4)":         0.4,
    "Cukup Yakin (0.6)":           0.6,
    "Yakin (0.8)":                 0.8,
    "Sangat Yakin (1.0)":          1.0,
}

# ── Section: Gejala ───────────────────────────────────────
st.markdown("""
<div style="background:white; border-radius:16px; padding:1.5rem;
            box-shadow:0 2px 12px rgba(21,128,61,0.07); border:1px solid #dcfce7; margin-bottom:1.5rem;">
    <h3 style="color:#15803d; margin-bottom:1rem; font-family:'Poppins',sans-serif;">📋 Daftar Gejala Tanaman</h3>
""", unsafe_allow_html=True)

input_user = {}

for g in daftar_gejala:
    col_input, col_badge = st.columns([5, 1])
    with col_input:
        # Menggunakan format string murni tanpa bold markdown di dalam agar tidak bentrok style-nya
        pilih = st.checkbox(
            f"{g['kode_gejala']} — {g['nama_gejala']}",
            key=f"cb_{g['id_gejala']}"
        )
        if pilih:
            bobot_pilihan = st.selectbox(
                f"Keyakinan untuk {g['kode_gejala']}:",
                options=list(opsi_keyakinan.keys()),
                key=f"sb_{g['id_gejala']}"
            )
            nilai_cf_user = opsi_keyakinan[bobot_pilihan]
            if nilai_cf_user != -1:
                input_user[g['id_gejala']] = nilai_cf_user
    with col_badge:
        if pilih:
            st.markdown(f"""
            <div style="background:#dcfce7; color:#15803d; border-radius:8px;
                        padding:0.3rem 0.6rem; font-size:0.75rem; font-family:'Poppins',sans-serif;
                        font-weight:600; text-align:center; margin-top:0.3rem;">✓ Dipilih</div>
            """, unsafe_allow_html=True)

    # Gambar jika ada
    nama_file_gambar = f"img/{g['kode_gejala']}.jpg"
    if os.path.exists(nama_file_gambar):
        st.image(nama_file_gambar, caption=f"Contoh {g['kode_gejala']}", width=130)

    st.markdown("<hr style='border-color:#f1f5f9; margin:0.5rem 0;'>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Selected summary ─────────────────────────────────────
if input_user:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7); border-radius:12px;
                padding:0.8rem 1.2rem; margin-bottom:1rem; border:1px solid #86efac;">
        <span style="font-family:'Poppins',sans-serif; font-weight:600; color:#15803d;">
            ✅ {len(input_user)} gejala dipilih
        </span>
        <span style="font-family:'Poppins',sans-serif; color:#64748b; font-size:0.88rem;">
            — siap untuk dihitung
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Calculate Button ─────────────────────────────────────
if st.button("🚀 Hitung Diagnosis Penyakit", type="primary", use_container_width=True):
    if not input_user:
        st.warning("⚠️ Silakan pilih minimal satu gejala terlebih dahulu!")
    else:
        # ── CF Calculation ─────────────────────────────────
        cf_per_penyakit = {}
        for rule in rules_cf:
            id_g = rule['id_gejala']
            id_p = rule['id_penyakit']
            if id_g in input_user:
                cf_he = float(rule['cf_pakar']) * input_user[id_g]
                cf_per_penyakit.setdefault(id_p, []).append(cf_he)

        # Kombinasi CF
        hasil_akhir = {}
        for id_p, list_cf in cf_per_penyakit.items():
            cf_kombinasi = list_cf[0]
            for i in range(1, len(list_cf)):
                cf_kombinasi = cf_kombinasi + list_cf[i] * (1 - cf_kombinasi)
            hasil_akhir[id_p] = cf_kombinasi

        hasil_urut = sorted(hasil_akhir.items(), key=lambda x: x[1], reverse=True)

        # ── Result Display ──────────────────────────────────
        st.markdown("---")
        st.markdown("<h3 style='color:#1e293b;'>📊 Hasil Diagnosis Sistem Pakar</h3>", unsafe_allow_html=True)

        if hasil_urut:
            id_p_tertinggi, nilai_cf = hasil_urut[0]
            persentase = nilai_cf * 100
            penyakit_terpilih = data_penyakit[id_p_tertinggi]

            # Status color
            if persentase <= 40:
                status_color = "#f59e0b"; status_bg = "#fffbeb"
                status_label = "⚠️ Kepastian Rendah"
            elif persentase <= 70:
                status_color = "#0ea5e9"; status_bg = "#f0f9ff"
                status_label = "ℹ️ Kepastian Sedang"
            else:
                status_color = "#22c55e"; status_bg = "#f0fdf4"
                status_label = "✅ Kepastian Tinggi"

            # Main result card
            st.markdown(f"""
            <div style="background:{status_bg}; border:2px solid {status_color}50;
                        border-radius:18px; padding:1.5rem 2rem; margin-bottom:1.5rem;
                        box-shadow: 0 4px 20px {status_color}10;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                    <div>
                        <div style="font-size:0.8rem; font-weight:600; color:{status_color};
                                    font-family:'Poppins',sans-serif; text-transform:uppercase;
                                    letter-spacing:0.05em; margin-bottom:0.4rem;">{status_label}</div>
                        <div style="font-size:1.5rem; font-weight:800; color:#1e293b;
                                    font-family:'Poppins',sans-serif; margin-bottom:0.3rem;">
                            {penyakit_terpilih['nama_penyakit']}
                        </div>
                        <div style="color:#475569; font-size:0.88rem; font-family:'Poppins',sans-serif;
                                    max-width:500px; line-height:1.6;">
                            {penyakit_terpilih['deskripsi']}
                        </div>
                    </div>
                    <div style="text-align:center; background:white; border-radius:16px;
                                padding:1rem 1.5rem; box-shadow:0 2px 8px rgba(0,0,0,0.05);
                                min-width:120px;">
                        <div style="font-size:2.2rem; font-weight:800; color:{status_color};
                                    font-family:'Poppins',sans-serif; line-height:1;">{persentase:.1f}%</div>
                        <div style="font-size:0.72rem; color:#94a3b8; font-family:'Poppins',sans-serif;
                                    margin-top:0.2rem;">Certainty Factor</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Solution card
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:1.3rem 1.5rem;
                        border-left:4px solid #22c55e; margin-bottom:1.5rem;
                        box-shadow:0 2px 10px rgba(21,128,61,0.08);">
                <div style="font-weight:700; color:#15803d; font-family:'Poppins',sans-serif;
                            margin-bottom:0.5rem; font-size:0.95rem;">💡 Solusi Penanganan Pakar</div>
                <div style="color:#334155; font-family:'Poppins',sans-serif; font-size:0.9rem; line-height:1.7;">
                    {penyakit_terpilih['solusi']}
                </div>
                <div style="margin-top:0.8rem; font-size:0.75rem; color:#94a3b8; font-family:'Poppins',sans-serif;">
                    📚 {penyakit_terpilih['referensi']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Bar chart alternatif
            if len(hasil_urut) > 1:
                st.markdown("<h4 style='color:#1e293b;'>📈 Perbandingan Semua Kemungkinan Penyakit</h4>", unsafe_allow_html=True)
                import pandas as pd
                df_grafik = pd.DataFrame({
                    "Penyakit": [data_penyakit[id_p]['nama_penyakit'] for id_p, _ in hasil_urut],
                    "Kepastian (%)": [round(v * 100, 2) for _, v in hasil_urut]
                })
                st.bar_chart(df_grafik.set_index("Penyakit"), color="#22c55e")

                with st.expander("📋 Lihat Rincian Alternatif Penyakit"):
                    for id_p_alt, val_alt in hasil_urut[1:]:
                        p = data_penyakit[id_p_alt]
                        pct = val_alt * 100
                        st.markdown(f"""
                        <div style="margin-bottom:0.7rem;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:0.2rem;">
                                <span style="font-family:'Poppins',sans-serif; font-weight:600;
                                             color:#334155; font-size:0.88rem;">{p['nama_penyakit']}</span>
                                <span style="font-family:'Poppins',sans-serif; font-weight:700;
                                             color:#64748b; font-size:0.88rem;">{pct:.1f}%</span>
                            </div>
                            <div style="background:#e2e8f0; border-radius:4px; height:6px; overflow:hidden;">
                                <div style="background:#84cc16; width:{pct}%; height:6px; border-radius:4px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Download report
            tgl_cetak = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            teks_laporan = (
                f"LAPORAN HASIL DIAGNOSA TANAMAN JAGUNG\n"
                f"{'='*45}\n"
                f"Tanggal  : {tgl_cetak}\n"
                f"Pengguna : {st.session_state.get('user_nama', 'User')}\n"
                f"{'='*45}\n\n"
                f"HASIL DIAGNOSA UTAMA\n"
                f"Penyakit : {penyakit_terpilih['nama_penyakit']}\n"
                f"Nilai CF  : {persentase:.2f}%\n\n"
                f"DESKRIPSI\n{penyakit_terpilih['deskripsi']}\n\n"
                f"SOLUSI PENANGANAN\n{penyakit_terpilih['solusi']}\n\n"
                f"REFERENSI\n{penyakit_terpilih['referensi']}\n"
            )
            st.download_button(
                label="📥 Unduh Laporan Diagnosa (.txt)",
                data=teks_laporan,
                file_name=f"Diagnosa_{penyakit_terpilih['nama_penyakit'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

            # Save to DB
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO diagnosa (id_user, tanggal, hasil_penyakit, nilai_cf) VALUES (%s, %s, %s, %s)",
                    (st.session_state['user_id'], tgl_cetak, penyakit_terpilih['nama_penyakit'], round(persentase, 2))
                )
                id_diagnosa_baru = cursor.lastrowid
                for id_gejala_u, cf_u_val in input_user.items():
                    cursor.execute(
                        "INSERT INTO detail_diagnosa (id_diagnosa, id_gejala, cf_user) VALUES (%s, %s, %s)",
                        (id_diagnosa_baru, id_gejala_u, cf_u_val)
                    )
                conn.commit()
                cursor.close()
                conn.close()
                st.success("✅ Hasil diagnosa berhasil disimpan ke riwayat!")
            except Exception as db_err:
                pass

        else:
            st.error("❌ Kombinasi gejala tidak mengarah ke penyakit manapun dalam basis pengetahuan.")