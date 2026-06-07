import json
import random
import string
import psycopg2
import psycopg2.errors
from http.server import HTTPServer, BaseHTTPRequestHandler
from db import get_db_connection, init_db

class ShortenerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/shorten":
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        original_url = data.get("url","").strip()
        if original_url == "" or not (original_url.startswith("http://") or original_url.startswith("https://")):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid URL"}')
            return

        characters = string.ascii_letters + string.digits
        # Adding to database
        conn = get_db_connection()

        while True:
            # random code generation
            short_code = "".join(random.choices(characters, k=6))
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
                        (short_code, original_url)
                    )
                conn.commit()
                break
            except psycopg2.errors.UniqueViolation:
                conn.rollback()

        conn.close()

        # Sending message approval
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response_data = {
            "short_code": short_code,
            "short_url": f"http://localhost:8000/{short_code}"
        }
        message = json.dumps(response_data)
        self.wfile.write(message.encode("utf-8"))
    
    def do_GET(self):
        pass
        
    def do_DELETE(self):
        pass

if __name__ == "__main__":
    init_db()
    server = HTTPServer(("localhost", 8000), ShortenerHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
