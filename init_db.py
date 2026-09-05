from config.database import get_db_connection

def init_db():
    conn = get_db_connection()
    if conn is None:
        print("❌ Gagal terhubung ke database Railway!")
        return

    cursor = conn.cursor()
    
    # Kueri membuat tabel users
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        location VARCHAR(100),
        hobbies TEXT,
        favorite_drink VARCHAR(100),
        favorite_music VARCHAR(100),
        profile_picture LONGBLOB
    );
    """
    
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ Tabel users berhasil dibuat/diverifikasi di Railway!")
    except Exception as e:
        print(f"❌ Error saat membuat tabel: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()