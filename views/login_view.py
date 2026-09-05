import streamlit as st
from controllers.auth_controller import AuthController

def render_login_view():
    st.title("🐾 Lupy Friends - Aplikasi Dating")
    
    # Inisialisasi state untuk menu pilihan jika belum ada
    if "auth_menu" not in st.session_state:
        st.session_state["auth_menu"] = "Login"
        
    # Memakai key="auth_menu" agar pilihan st.radio bisa diubah secara programmatic via session_state
    pilihan = st.radio(
        "Pilih Menu:", 
        ["Login", "Daftar Akun Baru"], 
        key="auth_menu", 
        horizontal=True
    )
    
    if pilihan == "Login":
        st.subheader("Login ke Akun Kamu")
        
        # Ambil username default dari session_state jika baru saja daftar
        default_user = st.session_state.get("registered_username", "")
        username = st.text_input("Username", value=default_user)
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
        
        st.write("---")
        foto_upload = st.file_uploader("Unggah Foto Profil Kamu (Format: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
        
        nama_file_foto = "default.png"
        
        if st.button("Daftar Sekarang"):
            if foto_upload is not None:
                import os
                folder_assets = os.path.join("views", "assets")
                if not os.path.exists(folder_assets):
                    os.makedirs(folder_assets)
                
                ekstensi = foto_upload.name.split(".")[-1]
                nama_file_foto = f"{username}_profile.{ekstensi}"
                path_simpan = os.path.join(folder_assets, nama_file_foto)
                
                with open(path_simpan, "wb") as f:
                    f.write(foto_upload.getbuffer())
            
            # Panggil fungsi register
            success = AuthController.register(username, password, nama, gender, hobi, minuman, musik, kota, nama_file_foto)
            
            # Jika registrasi berhasil (pastikan AuthController.register mengembalikan True saat sukses)
            if success:
                st.success("🎉 Registrasi berhasil! Mengalihkan ke halaman Login...")
                # Simpan username untuk auto-fill di form login
                st.session_state["registered_username"] = username
                # Ubah radio button ke 'Login' dan reload aplikasi
                st.session_state["auth_menu"] = "Login"
                st.rerun()