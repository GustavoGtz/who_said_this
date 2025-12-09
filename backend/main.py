from fastapi import FastAPI, UploadFile, File
from typing import List

from who.whatsapp.chat_reader import WhatsappReader
from who.models import Filter, Message

"""
How to open the endpoints:

> uv run uvicorn main:app --reload
"""

app = FastAPI(
    title="Who Said This API",
    description="POC API for reading WhatsApp chats",
    version="0.1.0",
)

wr: WhatsappReader | None = None

@app.post("/load_chat", summary="Load WhatsApp chat file")
async def load_chat(file: UploadFile = File(...)):
    global wr

    # Save uploaded file temporarily
    content = await file.read()
    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(content)

    wr = WhatsappReader(temp_path)

    return {"status": "chat loaded", "filename": file.filename}

@app.get("/get_members", summary="Return list of chat members")
async def get_members() -> List[str]:
    global wr
    if wr is None:
        return {"error": "Chat not loaded"}
    return wr.get_members()

@app.get("/get_messages_number", summary="Count messages using a filter")
async def get_messages_number(filter: Filter) -> int:
    global wr
    if wr is None:
        return {"error": "Chat not loaded"}
    return wr.get_messages_number(filter)


@app.get("/get_messages", summary="Get messages using a filter")
async def get_messages(filter: Filter) -> List[Message]:
    global wr
    if wr is None:
        return {"error": "Chat not loaded"}
    return list(wr.get_messages(filter))

