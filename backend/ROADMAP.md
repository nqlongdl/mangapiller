# 🗺️ Roadmap

## v2.0 — Multi-user Support
- [ ] Mỗi Discord user có favorites list riêng (manga + anime)
- [ ] DB refactor: thêm bảng `user_favorites(user_id, title, type)`
- [ ] Web UI: login bằng Discord OAuth, mỗi người quản lý list của mình
- [ ] Xem list của người khác trong cùng server

## v2.1 — Anime Support
- [ ] Fetch anime mới từ AniList GraphQL API (free, không cần scrape)
- [ ] Phân biệt type: `manga` vs `anime` trong DB
- [ ] Notify kèm episode number + thumbnail

## v2.2 — Discovery & Recommendations  
- [ ] Hiển thị trending manga/anime để user subscribe thêm
- [ ] Xem list của những người khác trong Discord server
- [ ] "X người trong server đang theo dõi Y"

## v2.3 — Notification UX
- [ ] Ping (@mention) những người subscribe khi có chapter/episode mới
- [ ] Gửi vào channel chung thay vì DM (configurable)
- [ ] Link trực tiếp để đọc/xem ngay
- [ ] Notification summary cuối ngày nếu có nhiều update