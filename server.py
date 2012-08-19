from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import mimetypes
import sqlite3

class CatteRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Starting GET handler")
        if self.path[:8] == '/images/':
            if self.path[8:] == 'random':
                self.handle_random_image()
            else:
                try:
                    self.handle_image(int(self.path[8:]))
                except ValueError:
                    self.send_error(404)
                    return
        elif self.path == '/random':
            self.handle_random()
        else:
            self.send_error(404)
            return

    def handle_image(self, number):
        db = sqlite3.connect('catte.db')
        image_info = db.execute('select image_url, image_data from raw_images where image_number=:image_number', {'image_number': number}).fetchone()
        self.image_processor(image_info)

    def handle_random_image(self):
        print("Starting handle_random_image")
        db = sqlite3.connect('catte.db')
        number = db.execute('select image_number from raw_images order by random() limit 1').fetchone()[0]
        image_info = db.execute('select image_url, image_data from raw_images where image_number=:image_number', {'image_number': number}).fetchone()
        self.image_processor(image_info)

    def handle_random(self):
        db = sqlite3.connect('catte.db')
        image_info = db.execute('select image_number from raw_images order by random() limit 1').fetchone()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        response_text = str(image_info[0]).encode('utf-8')
        self.send_header("Content-Length", len(response_text))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(response_text)

    def image_processor(self, image_info):
        if image_info is None:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-type", mimetypes.guess_type(image_info[0], False)[0])
        self.send_header("Content-Length", len(image_info[1]))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(image_info[1])

httpd = HTTPServer(('', 3333), CatteRequestHandler)
httpd.serve_forever()

