import streamlit as st
from controllers.auth_controller import AuthController

def render_login_view():
    st.title("🐾 Lupy Friends - Aplikasi Dating")
    
    menu = ["Login", "Daftar Akun Baru"]
    pilihan = st.radio("Pilih Menu:", menu, horizontal=True)
    
    if pilihan == "Login":
        st.subheader("Login ke Akun Kamu")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Masuk"):
            AuthController.login(username, password)
            
    elif pilihan == "Daftar Akun Baru":
        st.subheader("Form Pendaftaran")
        username = st.text_input("Buat Username")
        password = st.text_input("Buat Password", type="password")
        nama = st.text_input("Nama Lengkap")
        gender = st.selectbox("Gender", ["Pria", "Wanita"])
        kota = st.text_input("Kota Asal")
        hobi = st.text_input("Hobi (Pisahkan dengan koma jika banyak)")
        minuman = st.text_input("Minuman Favorit")
        musik = st.text_input("Genre Musik Favorit")
        
        # Opsi pilihan foto bawaan di folder assets
        # --- GANTI BAGIAN SELECTBOX FOTO LAMA DENGAN KODE DI BAWAH INI ---
        st.write("---")
        foto_upload = st.file_uploader("Unggah Foto Profil Kamu (Format: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
        
        # Default nama foto jika user tidak mengunggah apa-apa
        nama_file_foto = "default.png"
        
        if st.button("Daftar Sekarang"):
            if foto_upload is not None:
                import os
                # Membuat folder assets jika belum ada
                folder_assets = os.path.join("views", "assets")
                if not os.path.exists(folder_assets):
                    os.makedirs(folder_assets)
                
                # Biar nama fotonya unik dan tidak bentrok, kita gunakan username-nya sebagai nama file
                ekstensi = foto_upload.name.split(".")[-1]
                nama_file_foto = f"{username}_{nama_file_foto.replace('default.png', '')}.{ekstensi}"
                path_simpan = os.path.join(folder_assets, nama_file_foto)
                
                # Proses menyimpan file yang diupload ke folder assets
                with open(path_simpan, "wb") as f:
                    f.write(foto_upload.getbuffer())
            
            # Daftarkan ke database menggunakan nama file foto yang baru/default
            AuthController.register(username, password, nama, gender, hobi, minuman, musik, kota, nama_file_foto)