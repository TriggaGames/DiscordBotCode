import os
from dotenv import load_dotenv
from Client import Client

load_dotenv()
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

print("Bot Token: ", BOT_TOKEN)