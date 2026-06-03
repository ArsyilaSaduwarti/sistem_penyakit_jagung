from database.koneksi import get_connection

try:
    conn = get_connection()
    print("Koneksi database berhasil!")
    conn.close()
except Exception as e:
    print("Error:", e)