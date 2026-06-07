import json
import random
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
from db import get_db_connection, init_db

class ShortenerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/shorten":
            self.send_error(404, "Not Found")
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        data = json.loads(body)
        original_url = data.get("url","").strip()
        if original_url == "" or not (original_url.startswith("http://") or original_url.startswith("https://")):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid URL"}')
            return
        # losowy ciag 6 znakowy
        characters = string.ascii_letters + string.digits
        short_code = "".join(random.choices(characters, k=6))
        pass
    
    def do_GET(self):
        pass
        
    def do_DELETE(self):
        pass

if __name__ == "__main__":
    init_db()
    server = HTTPServer(("localhost", 8000), ShortenerHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
