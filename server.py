from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import mimetypes
import sqlite3

class CatteRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path[:8] == '/images/':
            self.handle_image(int(self.path[8:]))
        else:
            self.send_response(404)
            self.end_headers()
            return

    def handle_image(self, number):
        db = sqlite3.connect('catte.db')
        image_info = db.execute('select image_url, image_data from raw_images where image_number=:image_number', {'image_number': number}).fetchone()
        if image_info is None:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-type", mimetypes.guess_type(image_info[0], False)[0])
        self.send_header("Content-Length", len(image_info[1]))
        self.end_headers()
        self.wfile.write(image_info[1])

httpd = HTTPServer(('', 3333), CatteRequestHandler)
httpd.serve_forever()

