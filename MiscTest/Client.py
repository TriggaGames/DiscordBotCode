from discord import Client
from discord.message import Message

class MyClient(Client): 
    async def on_ready(self): 
        print(f'Loggd on as {self.user}')
        
    async def on_message(self, message: Message): 
        print(f'Message from {message.author}: {message.content}')
        