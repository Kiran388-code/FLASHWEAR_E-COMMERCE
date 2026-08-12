from typing import List
from fastapi import WebSocket

class ConnectionManager:
    """Connection manager for WebSockets to handle subscriptions and broadcasting."""
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Accept connection and add to active client pool."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove disconnected connection from client pool."""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """Send message directly to a single connection."""
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """Send message to all active connections."""
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

__all__ = ["ConnectionManager", "manager"]
