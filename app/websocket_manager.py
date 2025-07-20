import json
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.models import User, Message
from app.schemas import WebSocketMessage
from app.crud import create_message, get_messages_by_room
from app.auth import verify_token

class ConnectionManager:
    def __init__(self):
        # Store active connections by room_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store user info for each connection
        self.connection_users: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str, user: User):
        """Connect a user to a room."""
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        self.connection_users[websocket] = {
            "user_id": user.id,
            "username": user.username,
            "room_id": room_id
        }
        
        # Send join notification
        join_message = WebSocketMessage(
            type="join",
            content=f"{user.username} joined the room",
            room_id=room_id,
            user_id=user.id,
            username=user.username
        )
        await self.broadcast_to_room(room_id, join_message.dict())
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a user from a room."""
        if websocket in self.connection_users:
            user_info = self.connection_users[websocket]
            room_id = user_info["room_id"]
            username = user_info["username"]
            
            # Remove from active connections
            if room_id in self.active_connections:
                self.active_connections[room_id].remove(websocket)
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]
            
            # Remove user info
            del self.connection_users[websocket]
            
            # Send leave notification
            leave_message = WebSocketMessage(
                type="leave",
                content=f"{username} left the room",
                room_id=room_id,
                username=username
            )
            # Note: We can't broadcast here as the connection is already closed
            # This would need to be handled by the calling function
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific connection."""
        await websocket.send_text(message)
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        """Broadcast a message to all connections in a room."""
        if room_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.disconnect(connection)
    
    async def send_recent_messages(self, websocket: WebSocket, db: Session, room_id: str, limit: int = 50):
        """Send recent messages to a newly connected user."""
        messages = get_messages_by_room(db, room_id, limit=limit)
        
        for message in reversed(messages):  # Send in chronological order
            ws_message = WebSocketMessage(
                type="message",
                content=message.content,
                room_id=room_id,
                user_id=message.user_id,
                username=message.user.username
            )
            await self.send_personal_message(json.dumps(ws_message.dict()), websocket)

manager = ConnectionManager() 