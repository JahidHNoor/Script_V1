import contextlib
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import random
from tic_tac_toe.helpers import *
from tic_tac_toe.models import Tic_tac_toe_room

class GameConsumer(AsyncJsonWebsocketConsumer):
 
    board = {
       "0": '', "1": '', "2": '',
        "3": '', "4": '', "5": '',
        "6": '', "7": '', "8": '',
    }


    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f"group_{self.room_id}"
        room_from_model = await database_sync_to_async(Tic_tac_toe_room.objects.get)( id = self.room_id )
        player1_username = room_from_model.player1
        player2_username = room_from_model.player2
        

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(self.channel_name)


        tmpGroup = [player1_username, player2_username]
        print("Updated group members:", tmpGroup)

        if None in tmpGroup:
            print("Waiting for more players...")
        else:
            print("Game can start!1")


            
        first_player = random.choice(tmpGroup)
        print(first_player)
        await self.channel_layer.group_send(self.group_name, {
            "type": "gameData.send",
            "data": {
                "event": "game_start",
                "board": self.board,
                "turnUser": first_player,
                # "myTurn": False,
            }
        })

        print("Game can start!2")


    
    async def receive_json(self, content, **kwargs):
        print(content)
        room_from_model = await database_sync_to_async(Tic_tac_toe_room.objects.get)( id = self.room_id )
        player1_username = room_from_model.player1
        player2_username = room_from_model.player2

        if(content['event'] == "boardData_send"):
    
            winner = checkWin(content['board'])
            if(winner):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "won",
                        "board": content['board'],
                        "winner": winner,
                        "myTurn": False,
                    }
                })
            elif(isDraw(content['board'])):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "draw",
                        "board": content['board'],
                        "myTurn": False,
                    }
                })
            else:

                if content['lastTurn'] == player1_username:
                    turnUser = player2_username
                turnUser = player1_username
                await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "game_start",
                        "board": self.board,
                        "turnUser": turnUser,
                        # "myTurn": False,
                    }
                })

                print("Game can start!3")




        # elif(content['event'] == "restart"):

        #     # if(len(self.channel_layer.group_channels[self.group_name]) == 2):
        #     tmpGroup = list(self.channel_layer.groups[self.group_name])
        #     first_player = random.choice(tmpGroup)
        #     tmpGroup.remove(first_player)
        #     final_group = [first_player, tmpGroup[0]]
        #     for i, channel_name in enumerate(final_group):
        #         await self.channel_layer.send(channel_name, {
        #             "type": "gameData.send",
        #             "data": {
        #                 "event": "game_start",
        #                 "board": self.board,
        #                 "myTurn": True if i==0 else False
        #             }
        #         })

 
    async def disconnect(self, code):
        if(code==1):
            return 
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(self.group_name, {
            "type": "gameData.send",
            "data": {
                "event": "opponent_left",
                "board": self.board,
                "myTurn": False,
            }
        })
        

     
    async def gameData_send(self, context):
        await self.send_json(context['data'])
        
