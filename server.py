#!/usr/bin/env python3
"""Local server: serves static files + saves recordings to ./recordings/"""

import http.server
import os
import datetime

PORT = 8000
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), 'recordings')
os.makedirs(RECORDINGS_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save-recording':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            ext = 'webm' if b'webm' in self.headers.get('Content-Type', '').encode() else 'mp4'
            ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.join(RECORDINGS_DIR, f'laugh-{ts}.{ext}')
            with open(filename, 'wb') as f:
                f.write(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silent

if __name__ == '__main__':
    with http.server.HTTPServer(('', PORT), Handler) as httpd:
        print(f'Serving at http://localhost:{PORT}')
        httpd.serve_forever()
