## 💬 Chat Edukasi Judi Online


### 🗂 Struktur Proyek
```
fastapi_project/
│
├── app/
│   ├── main.py           # Entry point aplikasi  
│   ├── routes/
│   │   └── web.py        # Routing untuk halaman web
│   ├── templates/        # Template HTML
│   │   └── index.html    
│   └── static/           # File statis (CSS, JS, dll)
│       ├── css/
│       └── js/
│ 
├── requirements.txt      # Daftar dependensi Python
└── README.md             # Dokumentasi proyek
```

### 📦 Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/nama-kamu/fastapi-web-app.git
cd fastapi-web-app
```
2. Buat virtual environment dan aktifkan:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Install Dependensi:
```bash
pip install -r requirements.txt 
```

4. Jalankan Aplikasi:
```bash
uvicorn app.main:app --reload
```


