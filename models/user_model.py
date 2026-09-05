import streamlit as st
from config.database import get_db_connection

class UserModel:
    @staticmethod
    def register_user(username, password, nama, gender, hobi, minuman, musik, kota, foto="default.png"):
        """Fungsi untuk Fitur 2: Menyimpan user baru ke MySQL"""
        conn = get_db_connection()
        if not conn:
            st.error("❌ Gagal terhubung ke Database MySQL Railway.")
            return False
        
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, password, nama, gender, hobi, minuman_favorit, genre_musik, kota_asal, foto_profil)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (username, password, nama, gender, hobi, minuman, musik, kota, foto))
            conn.commit()
            return True
        except Exception as e:
            print(f"Gagal Register: {e}")
            st.error(f"❌ Detail Error DB: {e}")  # Tampilkan error asli di layar
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def login_user(username, password):
        """Fungsi untuk Fitur 1: Cek username & password di MySQL"""
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return user # Mengembalikan data user jika ada, atau None jika salah

    @staticmethod
    def update_profile(user_id, nama, hobi, minuman, musik, kota, foto=None):
        """Fungsi untuk Fitur 6: Edit profil sendiri"""
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        if foto:
            query = """
                UPDATE users 
                SET nama=%s, hobi=%s, minuman_favorit=%s, genre_musik=%s, kota_asal=%s, foto_profil=%s 
                WHERE id=%s
            """
            params = (nama, hobi, minuman, musik, kota, foto, user_id)
        else:
            query = """
                UPDATE users 
                SET nama=%s, hobi=%s, minuman_favorit=%s, genre_musik=%s, kota_asal=%s 
                WHERE id=%s
            """
            params = (nama, hobi, minuman, musik, kota, user_id)
            
        try:
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"Gagal Update Profil: {e}")
            st.error(f"❌ Error Update Profil: {e}")
            return False
        finally:
            cursor.close()
            conn.close()