import os
import socketserver
from functools import partial
from http.server import SimpleHTTPRequestHandler


def run_server(dir_to_serve_from: str = "docs", port: int = 8001):
    try:
        target_to = os.path.abspath(os.path.expanduser(dir_to_serve_from))

        handler = partial(SimpleHTTPRequestHandler, directory=target_to)

        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving '{target_to}' at http://localhost:{port}")
            httpd.serve_forever()

    except Exception as e:
        print(f"Error during server initialization: {e}")
