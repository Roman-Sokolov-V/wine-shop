import sys
import socket

try:
    sock = socket.create_connection(("localhost", 8000), timeout=3)
    sock.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
