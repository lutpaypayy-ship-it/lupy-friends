import streamlit as st
from models.swipe_model import SwipeModel
from models.user_model import UserModel
from controllers.swipe_controller import SwipeController
from controllers.auth_controller import AuthController
import os

def render_main_view():
    user_aktif = st.session_state['user_data']
    
    # --- SIDEBAR NAVIGASI (NAMA APK DIGANTI JADI LUPY FRIENDS) ---
    st.sidebar.title("Lupy Friends 🐾")
    st.sidebar.write(f"Halo, **{user_aktif['nama']}**!")
    menu = st.sidebar.radio("Navigasi Aplikasi", ["🏠 Beranda Swipe", "📥 Kotak Masuk Pesan", "👤 Edit Profil Saya", "🚪 Keluar"])
    
    # --- FITUR 5 & 3: BERANDA SWIPE ---
    if menu == "🏠 Beranda Swipe":
        st.header("Temukan Kecocokanmu ✨")
        profil_acak = SwipeModel.ambil_user_acak(user_aktif['id'])
        
        if profil_acak:
            st.write("---")
            
            # --- SISTEM PENGAMAN DAN PEMBACA FOTO PROFIL ---
            path_foto = os.path.join("views", "assets", profil_acak['foto_profil'])
            try:
                # Jika file fotonya ada di laptop DAN ukurannya bukan 0 KB, tampilkan foto asli
                if os.path.exists(path_foto) and os.path.getsize(path_foto) > 0:
                    st.image(path_foto, width=300)
                else:
                    # Jika file kosong/tidak ada, pakai avatar otomatis berbasis username dari internet
                    url_avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={profil_acak['username']}"
                    st.image(url_avatar, width=300)
            except Exception:
                # Cadangan darurat jika internet putus
                st.warning("Gagal memuat foto profil.")
                
            st.subheader(f"{profil_acak['nama']} ({profil_acak['gender']})")
            st.write(f"📍 **Asal:** {profil_acak['kota_asal']}")
            st.write(f"🎨 **Hobi:** {profil_acak['hobi']}")
            st.write(f"🍹 **Minuman Favorit:** {profil_acak['minuman_favorit']}")
            st.write(f"🎵 **Musik Favorit:** {profil_acak['genre_musik']}")
            st.write("---")
            
            # Input pesan saat LIKE
            pesan_input = st.text_input("Titip pesan buat dia? (Opsional)", placeholder="Hai, salam kenal...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💚 LIKE", use_container_width=True):
                    SwipeController.beri_aksi(profil_acak['id'], 'like', pesan_input)
            with col2:
                if st.button("❌ DISLIKE", use_container_width=True):
                    SwipeController.beri_aksi(profil_acak['id'], 'dislike')
        else:
            st.info("Wah, semua pengguna sudah kamu swipe! Coba cek lagi nanti.")

    # --- FITUR 4: KOTAK MASUK ---
    elif menu == "📥 Kotak Masuk Pesan":
        st.header("Kotak Masuk Kamu 📥")
        daftar_pesan = SwipeModel.ambil_kotak_masuk(user_aktif['id'])
        
        if daftar_pesan:
            for pm in daftar_pesan:
                with st.container():
                    st.write(f"**{pm['nama']}** menyukai profilmu!")
                    if pm['pesan']:
                        st.info(f"💬 Pesan: \"{pm['pesan']}\"")
                    else:
                        st.caption("(Dia tidak meninggalkan pesan)")
                    st.write("---")
        else:
            st.write("Belum ada pesan masuk nih. Tetap semangat swipe ya!")

    # --- FITUR 6: EDIT PROFIL ---
    elif menu == "👤 Edit Profil Saya":
        st.header("Pengaturan Profil Kamu ⚙️")
        
        # Ambil data terbaru dari DB
        user_db = UserModel.login_user(user_aktif['username'], user_aktif['password'])
        
        nama = st.text_input("Nama Lengkap", value=user_db['nama'])
        kota = st.text_input("Kota Asal", value=user_db['kota_asal'])
        hobi = st.text_input("Hobi", value=user_db['hobi'])
        minuman = st.text_input("Minuman Favorit", value=user_db['minuman_favorit'])
        musik = st.text_input("Genre Musik", value=user_db['genre_musik'])
        
        st.write("---")
        st.write(f"Foto Profil Saat Ini: `{user_db['foto_profil']}`")
        
        # --- PRATINJAU FOTO YANG TERDAFTAR ---
        path_foto_sekarang = os.path.join("views", "assets", user_db['foto_profil'])
        try:
            if os.path.exists(path_foto_sekarang) and os.path.getsize(path_foto_sekarang) > 0:
                st.image(path_foto_sekarang, width=150, caption="Foto Profil Aktif")
            else:
                st.image(f"https://api.dicebear.com/7.x/bottts/svg?seed={user_db['username']}", width=150, caption="Avatar Default")
        except Exception:
            st.caption("Gagal memuat pratinjau gambar.")

        foto_baru = st.file_uploader("Ganti Foto Profil Baru (Format: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
        
        if st.button("Simpan Perubahan"):
            nama_file_foto = user_db['foto_profil']  # default pakai foto yang lama
            
            # Jika user mengunggah foto baru saat edit profil
            if foto_baru is not None:
                folder_assets = os.path.join("views", "assets")
                if not os.path.exists(folder_assets):
                    os.makedirs(folder_assets)
                
                # Format nama file unik menggunakan username biar ga tabrakan
                ekstensi = foto_baru.name.split(".")[-1]
                nama_file_foto = f"{user_db['username']}_updated.{ekstensi}"
                path_simpan = os.path.join(folder_assets, nama_file_foto)
                
                with open(path_simpan, "wb") as f:
                    f.write(foto_baru.getbuffer())
            
            sukses = UserModel.update_profile(user_db['id'], nama, hobi, minuman, musik, kota, nama_file_foto)
            if sukses:
                st.success("Profil berhasil diperbarui!")
                # Perbarui data session agar perubahan langsung terasa di sidebar
                st.session_state['user_data'] = UserModel.login_user(user_aktif['username'], user_aktif['password'])
                st.rerun()
            else:
                st.error("Gagal memperbarui profil.")

    # --- LOGOUT ---
    elif menu == "🚪 Keluar":
        AuthController.logout()