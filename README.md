# Learning Management System (LMS) - Backend

## 📋 Deskripsi Proyek

Aplikasi Backend Learning Management System (LMS) ini dikembangkan menggunakan framework Django sebagai inti pengelolaan logika bisnis dan layanan aplikasi. Sistem backend berfungsi sebagai pusat pengolahan data, autentikasi pengguna, manajemen akademik, serta penyedia layana API yang terintegrasi dengan aplikasi frontend berbasis web.

Backend LMS dirancang untuk mendukung proses pembelajaran daring secara terstruktur, aman, dan efisien, dengan melibatkan berbagai peran pengguna seperti:

- **Administrator**
- **Dosen**
- **Mahasiswa**

## 🛠 Prasyarat

Pastikan sudah ter-install perangkat lunak berikut:

| Software       | Versi Minimum | Perintah Verifikasi      |
| -------------- | ------------- | ------------------------ |
| Docker         | ≥ 20.x        | `docker --version`       |
| Docker Compose | ≥ v2          | `docker compose version` |

## 🚀 Instalasi & Menjalankan Aplikasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Kukuh01/be-web-lms.git
cd be-web-lms
```

### 2️⃣ Konfigurasi Environment

Buat file `.env` di root project dengan konten berikut:

```env
DB_NAME=web_lms
DB_USER=lms_user
DB_PASSWORD=password123
DB_HOST=postgres
DB_PORT=5432

DEBUG=1
REDIS_HOST=redis
```

### 3️⃣ Build & Jalankan Container

```bash
# Build container
docker compose build

# Jalankan container (foreground)
docker compose up

# Atau jalankan di background
docker compose up -d
```

### 4️⃣ Setup Database

```bash
# Jalankan migrasi database
docker compose exec web python manage.py migrate
```

### 5️⃣ Buat Superuser (Admin)

```bash
docker compose exec web python manage.py createsuperuser
```

## 🌐 Akses Aplikasi

| Layanan                      | URL                             | Keterangan                |
| ---------------------------- | ------------------------------- | ------------------------- |
| Backend API / Web            | http://localhost:8000           | web interface             |
| Dokumentasi api Django Ninja | http://localhost:8000/api/docs  | Dokumentasi API endpoints |
| Django Admin                 | http://localhost:8000/admin     | Panel administrasi Django |
| Django Debug Toolbar         | Otomatis muncul di halaman HTML | Hanya di mode development |
| Django Silk                  | http://localhost:8000/silk/     | Profiling dan monitoring  |

## 🐳 Perintah Docker Penting

| Perintah                       | Fungsi                               |
| ------------------------------ | ------------------------------------ |
| `docker compose up`            | Menjalankan aplikasi                 |
| `docker compose down`          | Menghentikan dan menghapus container |
| `docker compose build`         | Build ulang image                    |
| `docker compose logs -f web`   | Melihat log aplikasi Django          |
| `docker compose exec web bash` | Masuk ke container web               |
| `docker compose ps`            | Melihat status container             |
| `docker compose restart`       | Restart semua container              |

## 🔧 Development Notes

### Fitur Development

- **DEBUG=True** diperlukan untuk:
  - Django Debug Toolbar
  - Django Silk
  - Fitur debugging lainnya
- Debug Toolbar tidak muncul di endpoint API JSON

### Komponen Sistem

- **Redis** digunakan untuk:
  - Session management
  - Caching
- **PostgreSQL** dijalankan dalam container terpisah

### Perintah Development Lainnya

```bash
# Membuat migrasi baru
docker compose exec web python manage.py makemigrations

# Menjalankan tests
docker compose exec web python manage.py test

# Mengumpulkan static files
docker compose exec web python manage.py collectstatic

# Untuk reset Database
docker compose exec web python manage.py reset_db

```

## 🔐 Production Deployment

### Konfigurasi Production

Untuk environment production:

1. Set `DEBUG=False`
2. Gunakan file environment terpisah: `.env.production`
3. Generate SECRET_KEY yang aman

### Optimasi Production

- **Nonaktifkan**:
  - Debug Toolbar
  - Django Silk
- **Gunakan reverse proxy** (Nginx/Apache)
- Konfigurasi SSL/TLS
- Setup backup database otomatis
- Monitoring dan logging yang robust

## 🤝 Kontribusi

1. Fork repository
2. Buat branch untuk fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Support

Jika mengalami masalah:

1. Cek logs aplikasi: `docker compose logs -f web`
2. Verifikasi container berjalan: `docker compose ps`
3. Pastikan port 8000 tidak digunakan aplikasi lain

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` file for more information.

## Struktur Folder

```text
├── apps
│   ├── accounts
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── auth.py
│   │   ├── management
│   │   ├── migrations
│   │   ├── models.py
│   │   └── schemas.py
│   ├── assignments
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── management
│   │   ├── migrations
│   │   └── models.py
│   ├── courses
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── management
│   │   ├── migrations
│   │   ├── models.py
│   │   └── services.py
│   ├── lessons
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── management
│   │   ├── migrations
│   │   ├── models.py
│   │   └── services.py
│   ├── submissions
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── management
│   │   ├── migrations
│   │   └── models.py
│   └── user
│       ├── dosen
│       └── mahasiswa
├── core
│   ├── api.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── jwt_auth.py
│   ├── management
│   │   ├── commands
│   │   └── __init__.py
│   ├── permissions.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── media
│   ├── submissions
│   └── thumbnails
├── README.md
└── requirements.txt

```
