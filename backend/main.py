import tempfile
import asyncio
from typing import List

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from who.whatsapp.chat_reader import WhatsappReader
from who.room.room import RoomManager
from who.models import (
    Filter,
    RoundMessage,
    RoomInitPayload,
    RoomRandomizeMessagesPayload,
    RoomSetSecondsPerRound
)

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


READER: WhatsappReader | None = None
ROOM: RoomManager | None = None

#whatsapp_messages: WhatsappMessagesManager | None = None
#room_manager: RoomManager = RoomManager()

# ########################################### #
#          API's for the READER               #
# ########################################### # 
@app.post("/api/reader/upload_chat", summary="Uploads the chat")
async def reader_upload_chat(file: UploadFile = File(...)):
    try:
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            temp_path = tmp.name

        global READER
        READER = WhatsappReader(temp_path)

        return {"status": "chat loaded", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/reader/get_members", summary="Return list of chat members")
async def reader_get_members() -> List[str]:
    global READER
    if READER is None: raise HTTPException(status_code=400, detail="Chat is not loaded")
    
    try:
        members = READER.get_members()
        return members
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/api/reader/get_messages_count", summary="Return the count of messages in the chat")
async def get_messages_count(filter: Filter) -> int:
    global READER
    if READER is None:
        raise HTTPException(status_code=400, detail="Chat is not loaded")
    
    try:
        messages_count = READER.get_messages_count(filter)
        return messages_count
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ########################################### #
#           API's for the ROOM                #
# ########################################### #
@app.post("/api/room/init", summary="Inits the room manager")
async def room_init(payload : RoomInitPayload) -> None:
    global READER
    global ROOM
    if READER is None:
        raise HTTPException(status_code=400, detail="Chat is not loaded")
    
    try:
        messages = READER.get_messages(payload.filter)
        ROOM = RoomManager(messages = messages, max_players = payload.max_players)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/room/get_max_players", summary="Return the number of max players of the room")
async def room_get_max_players() -> int:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        max_players = ROOM.get_max_players()
        return max_players
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@app.get("/api/room/get_messages_count", summary="Return the count of messages in the room")
async def room_get_messages_count() -> int:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        messages_count = ROOM.get_messages_count()
        return messages_count
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/room/randomize_messages", summary="Set the messages into randoms")
async def room_randomize_messages(payload : RoomRandomizeMessagesPayload) -> None:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        samples = ROOM.get_random_messages(number_of_messages = payload.number_of_messages)
        ROOM.set_messages(samples)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/api/room/set_seconds_per_round", summary="Set the messages into randoms")
async def set_seconds_per_round(payload : RoomSetSecondsPerRound) -> None:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        ROOM.set_seconds_per_round(payload.seconds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/room/get_seconds_per_round", summary="Return the seconds per round in the room")
async def room_get_seconds_per_round() -> int:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        seconds = ROOM.get_seconds_per_round()
        return seconds
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/room/get_round_message", summary="Return the message of the round (1 message and 4 answers)") 
async def room_get_round_message() -> RoundMessage:
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    try:
        round_message = ROOM.get_round_message()
        return round_message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    
# ########################################### #
#         WEBSOCKETS for the ROOM             #
# ########################################### #
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global ROOM
    if ROOM is None:
        raise HTTPException(status_code=400, detail="Room is not inited")
    
    await ws.accept()
    
    try:
        while True:
            msg = await ws.receive_json()
            msg_type = msg.get("type")
            
            # ########################################### #
            #           WEBSOCKETS OPERATIONS             #
            # ########################################### #
            
            # > Host a new party                          #
            if msg_type == "host":
                await ROOM.host_party(
                    host=ws,
                )
            
            # > Join to a party                          #
            if msg_type == "join":
                answer = await ROOM.join_party(
                    username= msg["username"],
                    client=ws
                )
                if not answer: # Error!
                    return
            
            # TODO: WS calls to the pool selection       #
                
            # > Start the game                           #  
            if msg_type == "start_game":
                answer = await ROOM.start_game()
                
                if not answer: # Error!
                    return
            
            # > Start the curtain                        #  
            if msg_type == "start_curtain":
                asyncio.create_task(ROOM.start_curtain())
            
            # > Finish the round                         #  
            if msg_type == "finish_round":
                asyncio.create_task(ROOM.finish_round())
            
            # > Start the question                       #  
            if msg_type == "question_start":
                ...
            
            # > End the question                         #  
            if msg_type == "question_end":
                ...
            
            # > Results of the question                  #  
            if msg_type == "question_result":
                ...
            
    except WebSocketDisconnect:
        await ROOM.remove_connection(ws)
