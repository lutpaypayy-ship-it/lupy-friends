import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="mysql.railway.internal",
            user="root",
            password="ptBdbHXWMXipHmeizKhOEcVacZvyGTHr",
            database="railway",
            port=3306,
            ssl_disabled=False  # Opsional: pastikan SSL aktif
        )
        return conn
    except Exception as e:
        print(f"Error Koneksi Database Cloud: {e}")
        return None