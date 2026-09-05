import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="mysql-1b358a98-lutpaypayy-2e7e.b.aivencloud.com",
            user="avnadmin",
            password="AVNS_btHCuD0GjjPDe9BoD-4",
            database="defaultdb",
            port=15414,
            ssl_disabled=False  # Opsional: pastikan SSL aktif
        )
        return conn
    except Exception as e:
        print(f"Error Koneksi Database Cloud: {e}")
        return None