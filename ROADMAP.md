# 🗺️ Roadmap

## v2.0 — Multi-user Support
- [ ] Each Discord user has their own favorites list (manga + anime)
- [ ] DB refactor: add `user_favorites(user_id, title, type)` table
- [ ] Web UI: Discord OAuth login, each user manages their own list
- [ ] View other users' lists within the same server

## v2.1 — Anime Support
- [ ] Fetch new anime episodes from AniList GraphQL API (free, no scraping needed)
- [ ] Distinguish type: `manga` vs `anime` in DB
- [ ] Notify with episode number + thumbnail

## v2.2 — Discovery & Recommendations
- [ ] Show trending manga/anime for users to subscribe to
- [ ] View lists of other members in the Discord server
- [ ] "X people in this server are tracking Y"

## v2.3 — Notification UX
- [ ] Ping (@mention) subscribers when a new chapter/episode drops
- [ ] Post to a shared channel instead of DM (configurable)
- [ ] Direct link to read/watch immediately
- [ ] End-of-day summary notification if there are multiple updates