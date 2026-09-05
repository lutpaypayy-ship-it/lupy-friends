@echo off
cd /d "D:\proyek gw bos"
call .venv\Scripts\activate

:: Jalankan Streamlit di latar belakang tanpa otomatis buka browser bawaan
start /b python -m streamlit run main.py --server.headless true

:: Tunggu 3 detik biar server Streamlit siap
timeout /t 3 /nobreak >nul

:: Buka aplikasi dengan mode "App" murni Chrome tanpa tombol navigasi browser
start chrome --app=http://localhost:8501

exit