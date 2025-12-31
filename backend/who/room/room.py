from fastapi import WebSocket
from typing import Sequence
from who.models import Message


class RoomManager:
    def __init__(self, messages : Sequence[Message], max_players : int):
        self.messages = messages
        self.max_players = max_players
        self.seconds_per_round = 100
        
        self.host = None
        self.clients = []
    
    # ########################################### #
    #           GAME related functions            #
    # ########################################### #
    def set_messages(self, new_messages : Sequence[Message]) -> None:
        self.messages = new_messages 
        
    def set_seconds_per_round(self, secs : int) -> None:
        self.seconds_per_round = secs
        
    def get_messages_count(self) -> int:
        return len(self.messages)
    
    def get_max_players(self) -> int:
        return self.max_players

    def get_random_messages(self, number_of_messages = int) -> Sequence[Message]:
        ...
        
    # ########################################### #
    #        WebSockets related functions         #
    # ########################################### #
    
    async def broadcast(self, data : dict, host : bool = True, clients : bool = True):
        targets = []
        
        if host: targets.append(self.host)
        if clients: targets += [c["ws"] for c in self.clients]
        
        for ws in targets:
            try:
                await ws.send_json(data)
            except Exception:
                pass
    
    async def host_party(self, host : WebSocket):
        if self.host is not None: 
            await host.send_json({
                "type": "error",
                "message": "The party is already being hosted!"
            })
            return
        
        self.host = host
        await host.send_json({
            "type" : "party_created",
            "message" : "The party was succesfuly created!"
        })
    
    async def join_party(self, username : str, client : WebSocket):
        if self.host is None:
            await client.send_json({
                "type" : "error",
                "message" : "The party is not being hosted!"
            })
            await client.close()
            return

        if len(self.clients) >= self.max_players:
            await client.send_json({
                "type" : "error",
                "message" : "The party is full!"
            })
            await client.close()
            return

        if any(c["username"] == username for c in self.clients):
            await client.send_json({
                "type" : "error",
                "message" : "The username is already taken!"
            })
            await client.close()
            return
        
        self.clients.append({
            "username" : username,
            "ws" : client
        })
        
        await self.broadcast({
            "type" : "user_joined",
            "players" : len(self.clients),
            "username" : username
        })
        
        return True
    
    async def remove_connection(self, ws: WebSocket):
        if self.host == ws:
            await self.broadcast({
                "type" : "room_closed",
                "message" : "The host closed the room!"
            })
            self.host = None
            self.clients = []
            return
        else:
            for client in self.clients:
                 if client["ws"] == ws:
                    self.clients.remove(client)
                        
                    await self.broadcast({
                        "type" : "user_left",
                        "message" : "A user left the party!",
                        "username" : client["username"]
                    })
                    return
                
    async def start_game(self):
        await self.broadcast({
            "type" : "game_started",
            "message" : "The game has started"
        })
        
                


