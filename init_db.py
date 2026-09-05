from config.database import get_db_connection

def setup_database():
    conn = get_db_connection()
    if conn is None:
        print("❌ Gagal terhubung ke database Aiven!")
        return
    
    cursor = conn.cursor()
    
    # Query Tabel Users
    query_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        nama VARCHAR(100) NOT NULL,
        gender VARCHAR(20),
        kota_asal VARCHAR(100),
        hobi VARCHAR(100),
        minuman_favorit VARCHAR(100),
        genre_musik VARCHAR(100),
        foto_profil VARCHAR(255) DEFAULT 'default.png'
    );
    """
    
    # Query Tabel Swipes
    query_swipes = """
    CREATE TABLE IF NOT EXISTS swipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        swiper_id INT NOT NULL,
        swipee_id INT NOT NULL,
        action ENUM('like', 'dislike') NOT NULL,
        pesan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (swiper_id) REFERENCES users(id),
        FOREIGN KEY (swipee_id) REFERENCES users(id)
    );
    """
    
    print("Sedang membuat tabel di Aiven...")
    cursor.execute(query_users)
    cursor.execute(query_swipes)
    conn.commit()
    
    print("✅ Berhasil! Tabel 'users' dan 'swipes' sudah dibuat di Aiven.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()