import json
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token, get_current_active_user
from app.crud import get_user_by_username, create_message, get_messages_by_room, delete_message
from app.schemas import Message, MessageCreate, WebSocketMessage
from app.websocket_manager import manager
from app.models import User

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str,
    token: Optional[str] = Query(None)
):
    """WebSocket endpoint for chat rooms with JWT authentication."""
    # Verify JWT token
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    token_data = verify_token(token)
    if not token_data:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Get database session
    db = next(get_db())
    
    # Get user from database
    user = get_user_by_username(db, token_data.username)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    try:
        # Connect to the room
        await manager.connect(websocket, room_id, user)
        
        # Send recent messages to the newly connected user
        await manager.send_recent_messages(websocket, db, room_id)
        
        # Handle incoming messages
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Validate message structure
                if "content" not in message_data or not message_data["content"].strip():
                    continue
                
                # Create message in database
                db_message = create_message(
                    db=db,
                    message=MessageCreate(
                        content=message_data["content"],
                        room_id=room_id
                    ),
                    user_id=user.id
                )
                
                # Broadcast message to all users in the room
                ws_message = WebSocketMessage(
                    type="message",
                    content=db_message.content,
                    room_id=room_id,
                    user_id=user.id,
                    username=user.username
                )
                await manager.broadcast_to_room(room_id, ws_message.dict())
                
            except json.JSONDecodeError:
                # Invalid JSON, ignore
                continue
            except Exception as e:
                # Log error and continue
                print(f"Error processing message: {e}")
                continue
                
    except WebSocketDisconnect:
        # Handle disconnect
        manager.disconnect(websocket)
        
        # Send leave notification to remaining users
        if websocket in manager.connection_users:
            user_info = manager.connection_users[websocket]
            leave_message = WebSocketMessage(
                type="leave",
                content=f"{user_info['username']} left the room",
                room_id=room_id,
                username=user_info['username']
            )
            await manager.broadcast_to_room(room_id, leave_message.dict())
    except Exception as e:
        # Handle any other errors
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
    finally:
        db.close()

@router.get("/messages/{room_id}", response_model=list[Message])
def get_room_messages(
    room_id: str,
    skip: int = 0,
    limit: int = 50,
    cursor: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get messages for a specific room with pagination."""
    messages = get_messages_by_room(db, room_id, skip=skip, limit=limit, cursor=cursor)
    return messages

@router.delete("/messages/{message_id}")
def delete_room_message(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a message (only by author or admin)."""
    success = delete_message(db, message_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or you don't have permission to delete it"
        )
    return {"message": "Message deleted successfully"} 