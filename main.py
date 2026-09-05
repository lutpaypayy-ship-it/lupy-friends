import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.login_view import render_login_view
from views.login_view import render_login_view
from views.main_view import render_main_view

# Mengubah nama di tab browser
st.set_page_config(page_title="Lupy Friends", page_icon="🐾", layout="centered")

def main():
    # --- TAMBAHKAN BARIS INI UNTUK MENGHANCURKAN CACHE LAMA ---
    st.cache_data.clear()
    st.cache_resource.clear()
    
    if 'user_data' not in st.session_state:
        # Panggil fungsi login
        render_login_view()
    else:
        render_main_view()

if __name__ == "__main__":
    main()