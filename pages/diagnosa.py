import streamlit as st
from database.koneksi import get_connection
from datetime import datetime
import os

st.title("🩺 Form Diagnosis Penyakit Jagung")
st.write("Silakan centang gejala tanaman jagung Anda dan tentukan tingkat keyakinannya.")

# 1. Ambil Data Master dari Database
conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM gejala")
daftar_gejala = cursor.fetchall()
cursor.execute("SELECT * FROM penyakit")
rows_p = cursor.fetchall()
data_penyakit = {p['id_penyakit']: p for p in rows_p}
cursor.execute("SELECT id_penyakit, id_gejala, cf_pakar FROM rules_cf")
rules_cf = cursor.fetchall()
cursor.close()
conn.close()

opsi_keyakinan = {
    "Pilih tingkat keyakinan...": -1,
    "Tidak Tahu": 0.0,
    "Sedikit Yakin": 0.4,
    "Cukup Yakin": 0.6,
    "Yakin": 0.8,
    "Sangat Yakin": 1.0
}

input_user = {}
st.subheader("📋 Daftar Gejala Tanaman:")

# Render Gejala dengan Layout Kolom (Kiri: Teks & Dropdown, Kanan: Foto Fisik Daun/Batang)
for g in daftar_gejala:
    col_input, col_img = st.columns([2, 1])
    
    with col_input:
        pilih = st.checkbox(f"**{g['kode_gejala']}** - {g['nama_gejala']}", key=f"cb_{g['id_gejala']}")
        if pilih:
            bobot_pilihan = st.selectbox(
                f"Tingkat keyakinan untuk {g['kode_gejala']}:",
                options=list(opsi_keyakinan.keys()),
                key=f"sb_{g['id_gejala']}"
            )
            nilai_cf_user = opsi_keyakinan[bobot_pilihan]
            if nilai_cf_user != -1:
                input_user[g['id_gejala']] = nilai_cf_user
                
    with col_img:
        # Menampilkan gambar contoh gejala jika file gambarnya ada di folder 'img/'
        nama_file_gambar = f"img/{g['kode_gejala']}.jpg"
        if os.path.exists(nama_file_gambar):
            st.image(nama_file_gambar, caption=f"Contoh {g['kode_gejala']}", width=150)
    st.write("---")

# 4. Proses Perhitungan Certainty Factor
if st.button("🚀 Hitung Diagnosis Penyakit", type="primary"):
    if not input_user:
        st.warning("⚠️ Silakan pilih minimal satu gejala terlebih dahulu!")
    else:
        cf_per_penyakit = {}

        # Kalkulasi CF Tunggal
        for rule in rules_cf:
            id_g = rule['id_gejala']
            id_p = rule['id_penyakit']
            
            if id_g in input_user:
                cf_user = input_user[id_g]
                cf_pakar = float(rule['cf_pakar'])
                cf_he = cf_pakar * cf_user
                
                if id_p not in cf_per_penyakit:
                    cf_per_penyakit[id_p] = []
                cf_per_penyakit[id_p].append(cf_he)

        # Kombinasi Nilai CF
        hasil_akhir = {}
        for id_p, list_cf in cf_per_penyakit.items():
            if len(list_cf) == 1:
                hasil_akhir[id_p] = list_cf[0]
            elif len(list_cf) > 1:
                cf_kombinasi = list_cf[0]
                for i in range(1, len(list_cf)):
                    cf_kombinasi = cf_kombinasi + list_cf[i] * (1 - cf_kombinasi)
                hasil_akhir[id_p] = cf_kombinasi

        hasil_urut = sorted(hasil_akhir.items(), key=lambda x: x[1], reverse=True)

        st.subheader("📊 Hasil Keputusan Sistem Pakar")
        if hasil_urut:
            id_p_tertinggi, nilai_cf = hasil_urut[0]
            persentase = nilai_cf * 100
            penyakit_terpilih = data_penyakit[id_p_tertinggi]

            # FITUR WARNA STATUS PRESENTASE BERDASARKAN SKOR KEPASTIAN
            if persentase <= 40:
                st.warning(f"Diagnosa Utama: Tanaman Anda terindikasi **{penyakit_terpilih['nama_penyakit']}** dengan akurasi Rendah.")
            elif persentase <= 70:
                st.info(f"Diagnosa Utama: Tanaman Anda terindikasi **{penyakit_terpilih['nama_penyakit']}** dengan akurasi Sedang.")
            else:
                st.success(f"Diagnosa Utama: Tanaman Anda POSITIF Terindikasi **{penyakit_terpilih['nama_penyakit']}**!")

            st.metric(label="Nilai Kepastian (Certainty Factor)", value=f"{persentase:.2f}%")
            st.write(f"💡 **Solusi Penanganan Pakar:**\n\n{penyakit_terpilih['solusi']}")

            # FITUR BAR CHART & KEMUNGKINAN PENYAKIT LAIN
            if len(hasil_urut) > 1:
                st.write("### 📈 Kemungkinan Penyakit Lain")
                
                # Menyiapkan data visualisasi bar chart
                nama_penyakit_list = [data_penyakit[id_p]['nama_penyakit'] for id_p, _ in hasil_urut]
                nilai_cf_list = [val * 100 for _, val in hasil_urut]
                
                df_grafik = {
                    "Nama Penyakit": nama_penyakit_list,
                    "Persentase Kepastian (%)": nilai_cf_list
                }
                st.bar_chart(data=df_grafik, x="Nama Penyakit", y="Persentase Kepastian (%)")
                
                # Tampilkan teks alternatif penyakit lain di bawah grafik
                with st.expander("Lihat Rincian Detail Alternatif Penyakit"):
                    for id_p_alt, nilai_cf_alt in hasil_urut[1:]:
                        st.write(f"- **{data_penyakit[id_p_alt]['nama_penyakit']}**: {nilai_cf_alt*100:.2f}%")

            # FITUR CETAK CETAK LAPORAN HASIL DIAGNOSA (.TXT / PRINT READY)
            tgl_cetak = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            teks_laporan = f"LAPORAN HASIL DIAGNOSA TANAMAN JAGUNG\n" \
                           f"Tanggal Pemeriksaan: {tgl_cetak}\n" \
                           f"Nama Pengguna: {st.session_state['user_nama']}\n" \
                           f"=========================================\n" \
                           f"Hasil Diagnosa Utama: {penyakit_terpilih['nama_penyakit']} ({persentase:.2f}%)\n" \
                           f"Solusi Pengobatan: {penyakit_terpilih['solusi']}\n"
                           
            st.download_button(
                label="📥 Cetak / Unduh Hasil Diagnosa (TXT)",
                data=teks_laporan,
                file_name=f"Hasil_Diagnosa_{penyakit_terpilih['nama_penyakit']}.txt",
                mime="text/plain"
            )

            # Simpan Riwayat ke DB
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO diagnosa (id_user, tanggal, hasil_penyakit, nilai_cf) VALUES (%s, %s, %s, %s)",
                    (st.session_state['user_id'], tgl_sekarang if 'tgl_sekarang' in locals() else tgl_cetak, penyakit_terpilih['nama_penyakit'], persentase)
                )
                id_diagnosa_terbaru = cursor.lastrowid
                for id_gejala_user, cf_user_val in input_user.items():
                    cursor.execute(
                        "INSERT INTO detail_diagnosa (id_diagnosa, id_gejala, cf_user) VALUES (%s, %s, %s)",
                        (id_diagnosa_terbaru, id_gejala_user, cf_user_val)
                    )
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as db_err:
                pass
        else:
            st.error("Kombinasi gejala tidak mengarah ke penyakit manapun dalam aturan basis pengetahuan.")