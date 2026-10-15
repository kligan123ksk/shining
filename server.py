from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import urllib.parse
import datetime

UPLOAD_DIR = 'uploads'


class SiteServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != '/upload':
            self.send_error(404)
            return

        params = urllib.parse.parse_qs(parsed.query)
        name = params.get('name', ['photo.jpg'])[0]
        name = os.path.basename(name).replace('\\', '_').replace('/', '_')
        if not name:
            name = 'photo.jpg'

        base, ext = os.path.splitext(name)
        if not ext:
            ext = '.jpg'

        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        path = os.path.join(UPLOAD_DIR, f'{base}-{stamp}{ext}')

        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)

        with open(path, 'wb') as f:
            f.write(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write('{"ok": true}'.encode('utf-8'))


if __name__ == '__main__':
    port = 8000
    print(f'Sайт запущен: http://localhost:{port}')
    HTTPServer(('', port), SiteServer).serve_forever()
