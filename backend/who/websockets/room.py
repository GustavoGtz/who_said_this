from fastapi import WebSocket
from typing import Dict


class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, dict] = {}

    async def broadcast(self, room: dict, data: dict, exclude: WebSocket = None):
        targets = [room["host"]] + [c["ws"] for c in room["clients"]]

        for ws in targets:
            if ws is exclude:
                continue
            try:
                await ws.send_json(data)
            except Exception:
                pass

    async def create_room(self, code: str, max_players: int, host: WebSocket):
        self.rooms[code] = {
            "host": host,
            "max_players": max_players,
            "clients": []
        }

        await host.send_json({
            "type": "room_created",
            "max_players": max_players,
            "code": code
        })

    async def join_room(self, code: str, name: str, client: WebSocket):
        if code not in self.rooms:
            await client.send_json({
                "type": "error",
                "code": "ROOM_NOT_FOUND",
                "message": "Room does not exist"
            })
            await client.close()
            return

        room = self.rooms[code]

        if len(room["clients"]) >= room["max_players"]:
            await client.send_json({
                "type": "error",
                "code": "ROOM_FULL",
                "message": "Room is full"
            })
            await client.close()
            return

        if any(c["name"] == name for c in room["clients"]):
            await client.send_json({
                "type": "error",
                "code": "NAME_TAKEN",
                "message": "Name already in use"
            })
            await client.close()
            return

        room["clients"].append({
            "name": name,
            "ws": client
        })

        await self.broadcast(room, {
            "type": "user_joined",
            "players": len(room["clients"]),
            "name": name
        })

        return True

    async def remove_connection(self, ws: WebSocket):
        for code, room in list(self.rooms.items()):

            if room["host"] == ws:
                await self.broadcast(room, {
                    "type": "room_closed"
                })
                del self.rooms[code]
                return

            for client in room["clients"]:
                if client["ws"] == ws:
                    room["clients"].remove(client)

                    await self.broadcast(room, {
                        "type": "user_left",
                        "name": client["name"]
                    })

                    return
