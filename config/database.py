import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="mysql.railway.internal",
            user="root",  # atau isi dari MYSQLUSER Railway
            password="ptBdbHXWMXipHmeizKhOEcVacZvyGTHr",
            database="railway",  # atau isi dari MYSQLDATABASE Railway
            port=3306  # ganti dengan angka dari MYSQLPORT Railway
        )
        return conn
    except Exception as e:
        print(f"Error Koneksi Database Railway: {e}")
        return None