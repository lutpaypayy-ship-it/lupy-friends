from config.database import get_db_connection

class SwipeModel:
    @staticmethod
    def simpan_swipe(swiper_id, swipee_id, action, pesan=""):
        """Fitur 3: Menyimpan aksi LIKE/DISLIKE dan pesan opsional"""
        conn = get_db_connection()
        if not conn: return False
        
        cursor = conn.cursor()
        query = """
            INSERT INTO swipes (swiper_id, swipee_id, action, pesan)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (swiper_id, swipee_id, action, pesan))
            conn.commit()
            return True
        except Exception as e:
            print(f"Gagal simpan swipe: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def ambil_user_acak(user_id):
        """Fitur 5: Mengambil 1 user acak yang BELUM PERNAH di-swipe"""
        conn = get_db_connection()
        if not conn: return None
        
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM users 
            WHERE id != %s 
            AND id NOT IN (SELECT swipee_id FROM swipes WHERE swiper_id = %s)
            ORDER BY RAND() LIMIT 1
        """
        cursor.execute(query, (user_id, user_id))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def ambil_kotak_masuk(user_id):
        """Fitur 4: Melihat siapa saja yang me-LIKE kita beserta pesannya"""
        conn = get_db_connection()
        if not conn: return []
        
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT users.nama, users.foto_profil, swipes.pesan, swipes.created_at 
            FROM swipes 
            JOIN users ON swipes.swiper_id = users.id 
            WHERE swipes.swipee_id = %s AND swipes.action = 'like'
            ORDER BY swipes.created_at DESC
        """
        cursor.execute(query, (user_id,))
        pesan_masuk = cursor.fetchall()
        cursor.close()
        conn.close()
        return pesan_masuk