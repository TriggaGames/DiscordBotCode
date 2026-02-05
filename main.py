import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from BaseBot import BaseBot

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
discord_ai_token = os.getenv("DISCORD_AI_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
ai = BaseBot(discord_ai_token)
ai.append_messages(
    "system",
    "You are an AI agent whos friendly and smart. Make sure to make each response a friendly and smart one."
    )
ai.talk_to_llm()

# secret_role = "Admin"

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
    # if "!clear" in message.content: 
    #     ai.clear_messages()
    #     message.reply("AI message history has been cleared!")
    # elif "!load" in message.content: 
    #     ai.load_messages()
    #     message.reply("AI message history had been loaded!")
    if bot.user in message.mentions: 
        # Make sure user message is in string format
        user_msg = str(message.content)
        
        # Store user message
        ai.append_messages(
            "user",
            user_msg
            )
        
        # Make conversation to LLM
        # Tell user thanks for messaging them
        await message.reply(f"{message.author}, thank you for the mention!")
        ai.talk_to_llm()
        messages = ai.get_messages()
        await message.reply(messages[-1].get("content"))
    
    await bot.process_commands(message)
    
@bot.command()
async def clear(msg): 
    ai.clear_messages()
    await msg.reply("AI chat history has been cleared!")
    
@bot.command()
async def load(msg): 
    ai.load_messages()
    await msg.reply("AI chat history had been loaded!")
    
# @bot.command()
# async def hello(ctx): 
#     await ctx.send(f'Hello {ctx.author.mention}!')
    
# @bot.command()
# async def assign(ctx): 
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role: 
#         await ctx.author.add_roles(role)
#         await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}.")
#     else: 
#         await ctx.send("Role doesn't exist")
    
# @bot.command()
# async def remove(ctx): 
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role: 
#         await ctx.author.remove_roles(role)
#         await ctx.send(f"{ctx.author.mention} has had the {secret_role} role removed.")
#     else: 
#         await ctx.send("Role doesn't exist")
    
# @bot.command()
# @commands.has_role(secret_role)
# async def secret(ctx):
#     await ctx.send("Welcome to the club!")
    
# @secret.error
# async def secret_error(ctx, error): 
#     if isinstance(error, commands.MissingRole): 
#         await ctx.send("You do not have permission to do that!")



bot.run(discord_bot_token, log_handler=handler, log_level=logging.DEBUG)