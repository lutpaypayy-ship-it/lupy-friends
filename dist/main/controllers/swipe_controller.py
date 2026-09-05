import streamlit as st
from models.swipe_model import SwipeModel

class SwipeController:
    @staticmethod
    def beri_aksi(swipee_id, action, pesan=""):
        swiper_id = st.session_state['user_id']
        sukses = SwipeModel.simpan_swipe(swiper_id, swipee_id, action, pesan)
        if sukses:
            st.toast(f"Berhasil melakukan {action}!")
            st.rerun()
        else:
            st.error("Gagal memproses swipe.")