from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile


from who.whatsapp.chat_reader import WhatsappReader
from who.websockets.room import RoomManager
from who.models import Filter, Message

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
        return {"error": "Chat not loaded"}
    return whatsapp_reader.get_members()

@app.get("/api/get_messages_number", summary="Count messages using a filter")
async def get_messages_number(filter: Filter) -> int:
    global whatsapp_reader
    if whatsapp_reader is None:
        return {"error": "Chat not loaded"}
    return whatsapp_reader.get_messages_number(filter)


@app.get("/api/get_messages", summary="Get messages using a filter")
async def get_messages(filter: Filter) -> List[Message]:
    global whatsapp_reader
    if whatsapp_reader is None:
        return {"error": "Chat not loaded"}
    return list(whatsapp_reader.get_messages(filter))


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
                    host=ws,
                )
            elif msg_type == "join":
                await room_manager.join_room(
                    code=msg["code"],
                    name=msg["name"],
                    client=ws
                )
        
    except WebSocketDisconnect:
        room_manager.remove_connection(ws)


    
