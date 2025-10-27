import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from functools import partial


def run_server(
    dir_to_serve_from: str = "public",
    port: int = 8000,
):
    try:
        target_to = os.path.abspath(os.path.expanduser(dir_to_serve_from))
        handler = partial(SimpleHTTPRequestHandler, directory=target_to)

        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"serving at port: {port}\n")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error during server initialization: {e}")
