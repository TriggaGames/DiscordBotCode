import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
discord_ai_token = os.getenv("DISCORD_AI_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Admin"

@bot.event
async def on_ready(): 
    print(f'We are ready to go in {bot.user.name}')
    
@bot.event
async def on_member_join(member): 
    await member.send(f'Welcome to the server, {member.name}')
    
@bot.event
async def on_message(message): 
    if message.author == bot.user: 
        return 
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")

    if "67" in message.content:
        await message.channel.send("https://tenor.com/view/bosnov-67-bosnov-67-67-meme-gif-16727368109953357722")
        
    if bot.user in message.mentions: 
        # Create AI instance
        client = OpenAI(
            api_key=discord_ai_token
        )

        response = client.responses.create(
            model="gpt-4.1",
            tools=[
                {
                    "type": "code_interpreter",
                    "container": {"type": "auto", "memory_limit": "4g"}
                }
            ],
            input=str(message.content),
            instructions="You are a friendly, smart AI. Respond to the user with something nice and make sure to answer their questions.",
            store=True
        )     
        
        reply = f'''Hello {message.author.mention}!
        
        {response.output_text}
        '''
        
        await message.reply(reply)
    
    await bot.process_commands(message)
    
@bot.command()
async def hello(ctx): 
    await ctx.send(f'Hello {ctx.author.mention}!')
    
@bot.command()
async def assign(ctx): 
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}.")
    else: 
        await ctx.send("Role doesn't exist")
    
@bot.command()
async def remove(ctx): 
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} role removed.")
    else: 
        await ctx.send("Role doesn't exist")
    
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")
    
@secret.error
async def secret_error(ctx, error): 
    if isinstance(error, commands.MissingRole): 
        await ctx.send("You do not have permission to do that!")



bot.run(discord_bot_token, log_handler=handler, log_level=logging.DEBUG)