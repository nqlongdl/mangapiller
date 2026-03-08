# 🥭 Manga Notifier

Tự động scrape [MangaPill](https://mangapill.com/chapters) và gửi Discord DM khi có chapter mới của manga yêu thích.

## ✨ Features
- Scrape MangaPill mỗi 24h
- Gửi Discord DM khi có chapter mới
- Web UI để quản lý danh sách manga yêu thích
- Dữ liệu lưu SQLite, persist qua Docker restart

## 🚀 Setup

### 1. Clone repo
```bash
git clone https://github.com/nqlongdl/mangapiller.git
cd mangapiller
```

### 2. Tạo Discord Bot
1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. New Application → Bot → Reset Token → copy token
3. Bật **Message Content Intent** nếu cần
4. Mời bot vào server (hoặc chỉ cần DM intent)

### 3. Tạo file .env
```bash
cp .env.example .env
```
Điền vào `.env`:
```env
DISCORD_TOKEN=your_bot_token
DISCORD_USER_ID=your_discord_user_id  # chuột phải vào tên mình → Copy User ID
CHECK_INTERVAL=86400                   # giây, mặc định 24h
```

### 4. Chạy
```bash
docker compose up --build
```
Web UI tại `http://localhost:8000`

## 📁 Cấu trúc project
```
├── backend/
│   ├── main.py       # Discord bot + scraper
│   ├── api.py        # FastAPI endpoints
│   ├── db.py         # SQLite
│   ├── config.py     # Load env
│   └── logger.py
├── frontend/
│   ├── src/
│   │   └── App.jsx   # React UI
│   └── index.html
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## 🔌 API
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/favorites` | Lấy danh sách manga |
| POST | `/api/favorites` | Thêm manga (`{"title": "..."}`) |
| DELETE | `/api/favorites` | Xóa manga (`{"title": "..."}`) |

## 📝 Lưu ý
- Tên manga phải **khớp một phần** với tên trên MangaPill (không phân biệt hoa thường)
- Sửa `.env` chỉ cần `docker compose up`, không cần `--build`
- `--build` chỉ cần khi sửa code