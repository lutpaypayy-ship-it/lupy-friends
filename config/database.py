import streamlit as st
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"])
        )
        return conn
    except Exception as e:
        print(f"Error DB Connection: {e}")
        st.error(f"❌ Error Detail Koneksi: {e}")  # Tampilkan penyebab gagal koneksi
        return None