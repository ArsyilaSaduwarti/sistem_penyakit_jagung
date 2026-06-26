import streamlit as st
from database.koneksi import get_connection

# Proteksi halaman agar user biasa tidak bisa menembak URL ini
if not st.session_state.get('logged_in') or st.session_state.get('user_role') != 'admin':
    st.error("Akses Ditolak! Halaman ini hanya untuk Administrator.")
    st.stop()

st.title("⚙️ Panel Manajemen Data Pakar")
st.caption("Gunakan halaman ini untuk memperbarui data master dan memantau riwayat pengguna.")

# Pembagian Tab Menu Admin
tab1, tab2, tab3, tab4 = st.tabs([
    "🦠 Kelola Penyakit", 
    "🌿 Kelola Gejala", 
    "🧬 Kelola Aturan (Rules CF)", 
    "📜 Riwayat Pengguna"
])

# ==========================================
# TAB 1: KELOLA PENYAKIT
# ==========================================
with tab1:
    st.header("Kelola Data Penyakit")
    with st.expander("➕ Tambah Penyakit Baru"):
        with st.form("form_tambah_penyakit", clear_on_submit=True):
            kode_p = st.text_input("Kode Penyakit", placeholder="Contoh: P07")
            nama_p = st.text_input("Nama Penyakit")
            deskripsi_p = st.text_area("Deskripsi Penyakit")
            solusi_p = st.text_area("Solusi Pengobatan")
            ref_p = st.text_input("Referensi Jurnal", placeholder="Contoh: Mahyuni (2021)")
            
            if st.form_submit_button("Simpan Penyakit", type="primary"):
                if kode_p and nama_p:
                    conn = get_connection()
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO penyakit (kode_penyakit, nama_penyakit, deskripsi, solusi, referensi) VALUES (%s, %s, %s, %s, %s)",
                            (kode_p, nama_p, deskripsi_p, solusi_p, ref_p)
                        )
                        conn.commit()
                        st.success(f"Penyakit {nama_p} berhasil disimpan!")
                    except Exception as e:
                        st.error(f"Gagal menyimpan: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.warning("Kode dan Nama Penyakit wajib diisi!")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM penyakit ORDER BY kode_penyakit ASC")
    data_penyakit = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if data_penyakit:
        st.dataframe(data_penyakit, use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: KELOLA GEJALA
# ==========================================
with tab2:
    st.header("Kelola Data Gejala")
    with st.expander("➕ Tambah Gejala Baru"):
        with st.form("form_tambah_gejala", clear_on_submit=True):
            kode_g = st.text_input("Kode Gejala", placeholder="Contoh: G23")
            nama_g = st.text_area("Detail/Nama Gejala")
            
            if st.form_submit_button("Simpan Gejala", type="primary"):
                if kode_g and nama_g:
                    conn = get_connection()
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO gejala (kode_gejala, nama_gejala) VALUES (%s, %s)", (kode_g, nama_g))
                        conn.commit()
                        st.success(f"Gejala {kode_g} berhasil disimpan!")
                    except Exception as e:
                        st.error(f"Gagal menyimpan: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.warning("Semua kolom wajib diisi!")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gejala ORDER BY id_gejala ASC")
    data_gejala = cursor.fetchall()
    cursor.close()
    conn.close()
    st.dataframe(data_gejala, use_container_width=True, hide_index=True)

# ==========================================
# TAB 3: KELOLA ATURAN (RULES CF)
# ==========================================
with tab3:
    st.header("Hubungkan Penyakit & Gejala (Rules)")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_penyakit, kode_penyakit, nama_penyakit FROM penyakit")
    opt_penyakit = cursor.fetchall()
    cursor.execute("SELECT id_gejala, kode_gejala, nama_gejala FROM gejala")
    opt_gejala = cursor.fetchall()
    cursor.close()
    conn.close()

    dict_p = {f"[{p['kode_penyakit']}] {p['nama_penyakit']}": p['id_penyakit'] for p in opt_penyakit}
    dict_g = {f"[{g['kode_gejala']}] {g['nama_gejala'][:50]}...": g['id_gejala'] for g in opt_gejala}

    with st.expander("➕ Hubungkan Aturan Baru"):
        with st.form("form_tambah_rule", clear_on_submit=True):
            pilih_p = st.selectbox("Pilih Penyakit", options=list(dict_p.keys()))
            pilih_g = st.selectbox("Pilih Gejala", options=list(dict_g.keys()))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                cf_pakar = st.number_input("CF Pakar", min_value=-1.0, max_value=1.0, value=0.0, step=0.1)
            with col2:
                mb = st.number_input("Nilai MB", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
            with col3:
                md = st.number_input("Nilai MD", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

            if st.form_submit_button("Simpan Aturan", type="primary"):
                id_p_terpilih = dict_p[pilih_p]
                id_g_terpilih = dict_g[pilih_g]
                
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO rules_cf (id_penyakit, id_gejala, cf_pakar, mb, md) VALUES (%s, %s, %s, %s, %s)",
                        (id_p_terpilih, id_g_terpilih, cf_pakar, mb, md)
                    )
                    conn.commit()
                    st.success("Aturan baru berhasil ditambahkan ke basis pengetahuan!")
                except Exception as e:
                    st.error(f"Gagal menambahkan aturan: {e}")
                finally:
                    cursor.close()
                    conn.close()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query_rules = """
        SELECT r.id_rule, p.kode_penyakit, p.nama_penyakit, g.kode_gejala, g.nama_gejala, r.cf_pakar, r.mb, r.md
        FROM rules_cf r
        JOIN penyakit p ON r.id_penyakit = p.id_penyakit
        JOIN gejala g ON r.id_gejala = g.id_gejala
        ORDER BY p.kode_penyakit ASC, g.kode_gejala ASC
    """
    cursor.execute(query_rules)
    data_rules = cursor.fetchall()
    cursor.close()
    conn.close()
    st.dataframe(data_rules, use_container_width=True, hide_index=True)

# ==========================================
# TAB 4: RIWAYAT DIAGNOSA PENGGUNA
# ==========================================
with tab4:
    st.header("Riwayat Hasil Diagnosa Pengguna")
    st.caption("Berikut adalah daftar hasil pemeriksaan tanaman jagung yang dilakukan oleh pengguna/petani.")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Kueri ini disesuaikan dengan kolom 'hasil_penyakit' dan 'nilai_cf' milik Anda
    query_riwayat = """
        SELECT d.id_diagnosa, u.nama AS nama_user, d.tanggal, d.hasil_penyakit, d.nilai_cf
        FROM diagnosa d
        JOIN users u ON d.id_user = u.id_user
        ORDER BY d.tanggal DESC
    """
    cursor.execute(query_riwayat)
    data_riwayat = cursor.fetchall()
    cursor.close()
    conn.close()

    if not data_riwayat:
        st.info("Belum ada riwayat diagnosa dari pengguna.")
    else:
        # Menampilkan tabel ringkasan riwayat utama
        st.dataframe(data_riwayat, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("🔍 Lihat Detail Gejala yang Dipilih")
        
        # Opsi dropdown untuk memilih ID Diagnosa yang ingin diintip gejalanya
        list_id_diagnosa = [f"ID {r['id_diagnosa']} - {r['nama_user']} ({r['tanggal']})" for r in data_riwayat]
        pilihan_detail = st.selectbox("Pilih Riwayat untuk melihat detail gejala:", list_id_diagnosa)
        
        if pilihan_detail:
            # Ambil ID saja dari teks string dropdown
            id_terpilih = int(pilihan_detail.split(" ")[1])
            
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Query untuk mengambil daftar gejala dan nilai inputan user (cf_user)
            query_detail = """
                SELECT g.kode_gejala, g.nama_gejala, dd.cf_user
                FROM detail_diagnosa dd
                JOIN gejala g ON dd.id_gejala = g.id_gejala
                WHERE dd.id_diagnosa = %s
            """
            cursor.execute(query_detail, (id_terpilih,))
            detail_gejala = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if detail_gejala:
                st.write(f"**Gejala yang dialami oleh pengguna pada pemeriksaan ini:**")
                st.dataframe(detail_gejala, use_container_width=True, hide_index=True)
            else:
                st.warning("Detail gejala untuk diagnosa ini tidak ditemukan.")