from fastapi import WebSocket
import random
from typing import Sequence
import asyncio
from who.models import Message, RoundMessage


class RoomManager:
    def __init__(self, messages : Sequence[Message], max_players : int):
        self.messages = messages
        self.members = self.get_members()
        self.max_players = max_players
        self.seconds_per_round = 20
        self.curtain_duration = 2 # seconds
        
        self.host = None
        self.clients = []
        
        self.round_message = None
        self.score_per_answer = 500
        self.round_answers_count = 0
        
    # ########################################### #
    #           GAME related functions            #
    # ########################################### #
    def set_messages(self, new_messages : Sequence[Message]) -> None:
        self.messages = new_messages 
        
    def set_seconds_per_round(self, secs : int) -> None:
        self.seconds_per_round = secs
    
    def get_members(self) -> Sequence[str]:
        members = []
        for message in self.messages:
            member = message.author
            if member not in members : members.append(member)
        return members
        
    def get_messages_count(self) -> int:
        return len(self.messages)
    
    def get_max_players(self) -> int:
        return self.max_players

    def get_seconds_per_round(self) -> int:
        return self.seconds_per_round
    
    def get_random_messages(self, number_of_messages = int) -> Sequence[Message]:
        return random.sample(self.messages, number_of_messages)
        
    def get_round_message(self): # Without the answer.
        return self.round_message
        
    def peak_message(self):
        msg = self.messages.pop(0)
        
        answer = msg.author
        
        options = [m for m in self.members if m != answer]
        options = random.sample(options, 3)
        options.append(answer)
        random.shuffle(options)
        
        self.round_message = RoundMessage(
            text = msg.text,
            time = msg.time,
            date = msg.date,
            answer = msg.author,
            options = options
        )
        print(self.round_message.text)
        
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
            "ws" : client,
            "score": 0
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
        return True

    async def finish_game(self):
        await self.broadcast({
            "type" : "game_finished",
            "message" : "The game has finished"
        })
    
    async def start_curtain(self):
        await self.broadcast({
            "type" : "curtain_started",
            "message" : "The curtain has started"
        })
        
        await asyncio.sleep(self.curtain_duration)
        
        await self.finish_curtain()
        
    async def finish_curtain(self):
        messages_count = len(self.messages)
        if messages_count > 0:
            await self.start_round()
        else:
            await self.finish_game()
    
    async def start_round(self):
        self.peak_message()
        self.round_answers_count = 0
        self.round_correct_answers = 0
        await self.broadcast({
            "type" : "round_started",
            "message" : "The round has started"
        })
    
    async def finish_round(self):
        await self.broadcast({
            "type" : "round_finished",
            "message" : "The round has finished",
            "answer" : self.round_message.answer
        })
    
    async def register_answer(self, client : WebSocket, answer : int):
        self.round_answers_count += 1
        
        is_correct = self.round_message.options[answer] == self.round_message.answer
        
        if is_correct:
            client_register = next((c for c in self.clients if c["ws"] is client), None)
            self.round_correct_answers += 1
            
            client_register["score"] += self.score_per_answer / self.round_correct_answers
        
        if self.round_answers_count >= len(self.clients):
            await self.finish_round()
        
    async def broadcast_scores(self) -> None:
        scores = [] 
        
        for client in self.clients:
            score = client["score"]
            username = client["username"]
            ws = client["ws"]
            
            score = {
                "type" : "score_showed",
                "username" : username,
                "score"    : score
            }
            
            scores.append(score)
            await ws.send_json(score)
            
        scores.sort(key=lambda s: s["score"], reverse=True)
        await self.host.send_json({
            "type": "scores_showed",
            "scores": scores
        })
  
        
        
        
            
             
        
        
        
                


