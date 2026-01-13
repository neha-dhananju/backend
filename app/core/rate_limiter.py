import time
from fastapi import Request, HTTPException

REQUEST_LIMIT = 60  # per minute
clients = {}


def rate_limit(request: Request):
    ip = request.client.host
    now = time.time()

    window = clients.get(ip, [])
    window = [t for t in window if now - t < 60]

    if len(window) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    window.append(now)
    clients[ip] = window
