"""Use this template for creating simple Python3 server"""

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def serve(port: int):
    if port > 65535:
        print(f"[X] port number, {port}, is not a valid port")
        print("[*] will use port 8888 instead")
        port = 8888
    Handler = SimpleHTTPRequestHandler
    with TCPServer(("", port), Handler) as httpd:
        print(f"[+] server running at http://localhost:{port}")
        httpd.serve_forever()
