import streamlit as st
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"]),
            connection_timeout=30,  # Beri waktu 30 detik agar Railway sempat bangun
            autocommit=True
        )
        return conn
    except Exception as e:
        print(f"Error DB Connection: {e}")
        st.error(f"❌ Error Detail Koneksi: {e}")
        return None