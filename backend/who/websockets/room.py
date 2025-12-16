from fastapi import WebSocket
from typing import List


class RoomManager:
    def __init__(self):
        self.rooms = {}
    
    async def create_room(self, code : str, host : WebSocket):
        self.rooms[code] = {
            "host"    : host,
            "clients" : []
        } 
        
        await host.send_json(
            {
                "type" : "room_created",
                "code" : code,
            }
        )
    
    async def join_room(self, code : str, name : str, client : WebSocket):
        if code not in self.rooms:
            await client.send_json({
                "type"    : "error",
                "message" : "Room does not exist"
            })
            return
        
        room = self.rooms[code]
        room["clients"].append({
            "name" : name,
            "ws"   : client
        })
        
        await room["host"].send_json({
            "type": "user_joined",
            "name": name
        })

        await client.send_json({
            "type": "joined",
            "name": name
        })
    
    def remove_connection(self, ws: WebSocket):
        for code, room in list(self.rooms.items()):
            if room["host"] == ws:
                del self.rooms[code]
                return

            room["clients"] = [
                c for c in room["clients"] if c["ws"] != ws
            ]