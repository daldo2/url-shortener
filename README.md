# URL Shortener

A simple link-shortening service in Python: `http.server` (standard library) + PostgreSQL.

> **Status: work in progress.** URL validation and short-code generation are done;
> saving to the database, redirects (`GET`) and deleting (`DELETE`) are still to do.

## API (planned)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/shorten` | Body `{"url": "https://..."}` → returns a random 6-character code. Invalid URL → `400`. |
| `GET` | `/<code>` | Redirects to the original URL and counts the click. |
| `DELETE` | `/<code>` | Deletes the short link. |

## Database

Table `urls`: `id`, `short_code` (unique), `original_url`, `created_at`, `click_count`.
It is created automatically on server start (`init_db()` in `db.py`).

## Running

Requirements: Python 3, PostgreSQL running locally with a database `url_shortener_db` (user `postgres`).

```bash
pip install psycopg2-binary
python server.py        # http://localhost:8000
```
