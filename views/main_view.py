import streamlit as st
from models.swipe_model import SwipeModel
from models.user_model import UserModel
from controllers.swipe_controller import SwipeController
from controllers.auth_controller import AuthController
import os
import yt_dlp

# --- FUNGSI PENCARIAN & EKSTRAK URL YOUTUBE ---
def cari_dan_ambil_audio(judul_lagu):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'n_entries': 1
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{judul_lagu}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
                # Mengembalikan URL YouTube asli (webpage_url) dan judulnya
                return video_info.get('webpage_url', f"https://www.youtube.com/watch?v={video_info['id']}"), video_info.get('title', judul_lagu)
            return None, None
    except Exception:
        return None, None

def render_main_view():
    user_aktif = st.session_state['user_data']

    # --- SIDEBAR NAVIGASI ---
    st.sidebar.title("Lupy Friends 🐾")
    st.sidebar.write(f"Halo, **{user_aktif['nama']}**!")
    menu = st.sidebar.radio("Navigasi Aplikasi", ["🏠 Beranda Swipe", "📥 Kotak Masuk Pesan", "👤 Edit Profil Saya", "🚪 Keluar"])
    
    # --- FITUR REQ JUDUL LAGU (SIDEBAR) ---
    st.sidebar.write("---")
    st.sidebar.subheader("🎵 Cari & Putar Lagu")
    
    judul_input = st.sidebar.text_input("Ketik Judul Lagu / Penyanyi:", placeholder="Contoh: Kalah - Slank", key="input_judul_lagu_lupy")
    
    if 'audio_stream_aktif' not in st.session_state:
        st.session_state['audio_stream_aktif'] = None
    if 'judul_lagu_aktif' not in st.session_state:
        st.session_state['judul_lagu_aktif'] = None
        
    if st.sidebar.button("🔍 Cari & Putar", use_container_width=True):
        if judul_input.strip() != "":
            with st.sidebar.spinner("Mencari lagu di YouTube..."):
                stream_url, judul_ketemu = cari_dan_ambil_audio(judul_input)
                if stream_url:
                    st.session_state['audio_stream_aktif'] = stream_url
                    st.session_state['judul_lagu_aktif'] = judul_ketemu
                    st.sidebar.success(f"Ditemukan: {judul_ketemu}")
                    st.rerun()
                else:
                    st.sidebar.error("Lagu tidak ditemukan. Coba ketik judul lain, bro!")
        else:
            st.sidebar.warning("Ketik dulu judul lagunya, bro!")
            
    # TAMPILKAN VIDEO PLAYER YOUTUBE RESMI (ANTI-ERROR CORS/PLAYBACK)
    if st.session_state['audio_stream_aktif']:
        st.sidebar.caption(f"📻 Now Playing:\n**{st.session_state['judul_lagu_aktif']}**")
        st.sidebar.video(st.session_state['audio_stream_aktif'])
        
        if st.sidebar.button("🗑️ Matikan Musik", use_container_width=True):
            st.session_state['audio_stream_aktif'] = None
            st.session_state['judul_lagu_aktif'] = None
            st.rerun()

    # --- FITUR 5 & 3: BERANDA SWIPE ---
    if menu == "🏠 Beranda Swipe":
        st.header("Temukan Kecocokanmu ✨")
        
        # --- KOMPONEN FILTER GENRE ---
        st.write("⚙️ **Filter Pencarian Teman**")
        list_genre = ["Semua", "Pop", "Rock", "RnB", "Dangdut", "Indie", "Hip Hop"]
        genre_terpilih = st.selectbox("Pilih Aliran Musik Pengguna yang Ingin Dicari:", list_genre, key="filter_genre_musik_swipe")
        
        profil_acak = SwipeModel.ambil_user_acak(user_aktif['id'], genre_filter=genre_terpilih)
        
        if profil_acak:
            st.write("---")
            
            path_foto = os.path.join("views", "assets", profil_acak['foto_profil'])
            try:
                if os.path.exists(path_foto) and os.path.getsize(path_foto) > 0:
                    st.image(path_foto, width=300)
                else:
                    url_avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={profil_acak['username']}"
                    st.image(url_avatar, width=300)
            except Exception:
                st.warning("Gagal memuat foto profil.")
                
            st.subheader(f"{profil_acak['nama']} ({profil_acak['gender']})")
            st.write(f"📍 **Asal:** {profil_acak['kota_asal']}")
            st.write(f"🎨 **Hobi:** {profil_acak['hobi']}")
            st.write(f"🍹 **Minuman Favorit:** {profil_acak['minuman_favorit']}")
            st.write(f"🎵 **Musik Favorit:** {profil_acak['genre_musik']}")
            st.write("---")
            
            pesan_input = st.text_input("Titip pesan buat dia? (Opsional)", placeholder="Hai, salam kenal...", key="pesan_dating_lupy_fixed")
            
            if st.button("✉️ Kirim Pesan Saja", use_container_width=True, key="kirim_manual_bro_fixed"):
                if pesan_input.strip() != "":
                    SwipeController.beri_aksi(profil_acak['id'], 'like', pesan_input)
                    st.toast(f"💬 Pesan terkirim ke {profil_acak['nama']}!", icon="🚀")
                    st.success(f"Sukses mengirim pesan: \"{pesan_input}\". Sekarang kamu bisa LIKE atau lanjut DISLIKE!")
                else:
                    st.warning("Ketik dulu pesannya di kolom atas, baru klik tombol kirim, bro!")
            
            st.write("") 
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💚 LIKE PROFILE", use_container_width=True, key="like_murni_final_bgt_fixed"):
                    SwipeController.beri_aksi(profil_acak['id'], 'like', "")
                    st.rerun()
            with col2:
                if st.button("❌ DISLIKE", use_container_width=True, key="dislike_murni_final_bgt_fixed"):
                    SwipeController.beri_aksi(profil_acak['id'], 'dislike')
                    st.rerun()
                    
        else:
            st.info(f"Wah, tidak ada pengguna dengan genre musik '{genre_terpilih}' yang tersisa untuk di-swipe!")

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
        user_db = UserModel.login_user(user_aktif['username'], user_aktif['password'])
        
        nama = st.text_input("Nama Lengkap", value=user_db['nama'])
        kota = st.text_input("Kota Asal", value=user_db['kota_asal'])
        hobi = st.text_input("Hobi", value=user_db['hobi'])
        minuman = st.text_input("Minuman Favorit", value=user_db['minuman_favorit'])
        musik = st.text_input("Genre Musik", value=user_db['genre_musik'])
        
        st.write("---")
        st.write(f"Foto Profil Saat Ini: `{user_db['foto_profil']}`")
        
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
            nama_file_foto = user_db['foto_profil']
            if foto_baru is not None:
                folder_assets = os.path.join("views", "assets")
                if not os.path.exists(folder_assets):
                    os.makedirs(folder_assets)
                ekstensi = foto_baru.name.split(".")[-1]
                nama_file_foto = f"{user_db['username']}_updated.{ekstensi}"
                path_simpan = os.path.join(folder_assets, nama_file_foto)
                with open(path_simpan, "wb") as f:
                    f.write(foto_baru.getbuffer())
            
            sukses = UserModel.update_profile(user_db['id'], nama, hobi, minuman, musik, kota, nama_file_foto)
            if sukses:
                st.success("Profil berhasil diperbarui!")
                st.session_state['user_data'] = UserModel.login_user(user_aktif['username'], user_aktif['password'])
                st.rerun()
            else:
                st.error("Gagal memperbarui profil.")

    # --- LOGOUT ---
    elif menu == "🚪 Keluar":
        AuthController.logout()