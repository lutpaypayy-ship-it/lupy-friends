import mysql.connector

def get_db_connection():
    try:
        # Salin string dari MYSQL_PUBLIC_URL di Railway
        url = "mysql://root:ptBdbHXWMXipHmeizKhOEcVacZvyGTHr@reseau.proxy.rlwy.net:45307/railway" 
        
        # Contoh formatnya nanti seperti ini:
        # url = "mysql://root:password@junction.proxy.rlwy.net:12345/railway"
        
        # Parsing URL publik
        url = url.replace("mysql://", "")
        auth, rest = url.split("@")
        user, password = auth.split(":")
        host_port, database = rest.split("/")
        host, port = host_port.split(":")

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port)
        )
        return conn
    except Exception as e:
        print(f"Error Koneksi Database Railway: {e}")
        return None