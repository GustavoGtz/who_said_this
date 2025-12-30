from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile

from who.whatsapp.chat_reader import WhatsappReader
from who.whatsapp.messages_manager import WhatsappMessagesManager
from who.websockets.room import RoomManager
from who.models import Filter, Message, RoomInit, Integer

from pydantic import BaseModel


"""
How to open the endpoints:

> uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

app = FastAPI(
    title="Who Said This API",
    description="POC API for reading WhatsApp chats",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # frontend Vue (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


whatsapp_reader: WhatsappReader | None = None
whatsapp_messages: WhatsappMessagesManager | None = None
room_manager: RoomManager = RoomManager()


@app.post("/api/load_chat")
async def load_chat(file: UploadFile = File(...)):
    try:
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            temp_path = tmp.name

        global whatsapp_reader
        whatsapp_reader = WhatsappReader(temp_path)

        return {"status": "chat loaded", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/get_members", summary="Return list of chat members")
async def get_members() -> List[str]:
    global whatsapp_reader
    
    if whatsapp_reader is None:
        raise HTTPException(status_code=400, detail="Chat not loaded")
    
    try:
        members = whatsapp_reader.get_members()
        return members
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/get_max_players", summary="Return the number of max players of the game")
async def get_members() -> int:
    global whatsapp_messages
    
    if whatsapp_messages is None:
        raise HTTPException(status_code=400, detail="Game not init")
    
    try:
        max_players = whatsapp_messages.get_max_players()
        return max_players
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/get_messages_number", summary="Count messages using a filter")
async def get_messages_number(filter: Filter) -> int:
    global whatsapp_reader

    if whatsapp_reader is None:
        raise HTTPException(status_code=400, detail="Chat not loaded")
    
    try:
        n_messages = whatsapp_reader.get_messages_number(filter)
        return n_messages
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/init_room", summary="Init the room/messages controller")
async def init_room(ri : RoomInit) -> None:
    global whatsapp_reader
    global whatsapp_messages
    if whatsapp_reader is None:
        raise HTTPException(status_code=400, detail="Chat not loaded")
    
    try:
        messages = whatsapp_reader.get_messages(ri.filters)
        whatsapp_messages = WhatsappMessagesManager(messages, ri.max_players)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/get_room_messages_number", summary="Return the number of messages in the party")
async def get_room_messages_number() -> int:
    global whatsapp_messages
    
    if whatsapp_messages is None:
        raise HTTPException(status_code=400, detail="Game not init")
    
    try:
        messages_number = whatsapp_messages.get_messages_number()
        return messages_number
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/set_random_messages", summary="Set the messages into randoms")
async def set_random_messages(n : Integer) -> None:
    global whatsapp_messages
    if whatsapp_messages is None:
        raise HTTPException(status_code=400, detail="Game not init")
    
    try:
        samples = whatsapp_messages.get_random(n.number)
        whatsapp_messages.set_messages(samples)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    

# APPI para setupear los settings del la partida.

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    
    try:
        while True:
            msg = await ws.receive_json()
            
            msg_type = msg.get("type")
            
            if msg_type == "host":
                await room_manager.create_room(
                    code=msg["code"],
                    max_players= whatsapp_messages.get_max_players(),
                    host=ws,
                )
            elif msg_type == "join":
                ok = await room_manager.join_room(
                    code=msg["code"],
                    name=msg["name"],
                    client=ws
                )
                if not ok:
                    return
            elif msg_type == "start_game":
                await room_manager.broadcast(
                    code=msg["code"],
                    data={
                        "type" : "game_started"
                    }
                )
    except WebSocketDisconnect:
        await room_manager.remove_connection(ws)


    
