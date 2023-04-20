import http.server
import socketserver
import socket
import argparse

parser = argparse.ArgumentParser(description='Serve a file over HTTP')
parser.add_argument('file', type=str, help='The file to serve')

# Specify the file you want to serve
file_path = parser.parse_args().file

# Create a handler for serving the file
class FileHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Override the default behavior to send the specified file
        if self.path != "/file":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-type", "text/csv")
        self.end_headers()
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

# Create a server object to listen on port 8000
print(f"Serving {file_path} at http://localhost:8000/file")
with socketserver.TCPServer(("", 8000), FileHandler) as httpd:
    print("serving at port 8000")
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    httpd.serve_forever()