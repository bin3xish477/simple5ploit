"""Use this template for creating simple Python3 server"""

from http.server import SimpleHTTPRequestHanlder
from socketserver import TCPServer

def serve(port: int):
  with TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
      print(f"server running on :{port}")
      httpd.serve_forever()
