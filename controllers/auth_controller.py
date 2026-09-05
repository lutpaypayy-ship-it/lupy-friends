import streamlit as st
from models.user_model import UserModel

class AuthController:
    @staticmethod
    def login(username, password):
        user = UserModel.login_user(username, password)
        if user:
            st.session_state['user_id'] = user['id']
            st.session_state['user_data'] = user
            st.success(f"Selamat datang kembali, {user['nama']}!")
            st.rerun()
        else:
            st.error("Username atau Password salah!")

    @staticmethod
    def register(username, password, nama, gender, hobi, minuman, musik, kota, foto):
        sukses = UserModel.register_user(username, password, nama, gender, hobi, minuman, musik, kota, foto)
        if sukses:
            st.success("Pendaftaran berhasil! Silakan ke menu Login.")
            return True
        else:
            # st.error sudah ditangani langsung oleh UserModel jika ada error spesifik
            return False

    @staticmethod
    def logout():
        st.session_state.clear()
        st.rerun()