import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="reseau.proxy.rlwy.net",
            user="root",
            password="ptBdbHXWMXipHmeizKhOEcVacZvyGTHr",
            database="railway",
            port=45307
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error Koneksi Database Cloud: {err}")
        return None