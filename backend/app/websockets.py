from typing import List

from fastapi import WebSocket

active_connections: List[WebSocket] = []

async def broadcast(message: dict):
    for connection in active_connections.copy():
        try:
            await connection.send_json(message)
        except Exception:
            if connection in active_connections:
                active_connections.remove(connection)

async def connect_ws(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)

def disconnect_ws(ws: WebSocket):
    if ws in active_connections:
        active_connections.remove(ws)
