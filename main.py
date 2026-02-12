# Necessary imports
import discord
import io
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

# Script imports
from NotesHandler import NotesHandler
from AIBot import AIBot

# TODO: Add developer mode
# TODO: Add message history
# TODO: Add clear history
# TODO:
# Add notes
# TODO: Add show notes
# TODO: Add clear notes

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
discord_ai_token = os.getenv("DISCORD_AI_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Main discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Helper bots
ai = AIBot(discord_ai_token)
ai.append_messages(
    "system",
    "You are an AI agent whos friendly and smart. Make sure to make each response a friendly and smart one."
    )
ai.talk_to_llm()
nh = NotesHandler()

# Helper functions
def msg_to_file(msg: str, filename: str): 
    # Send response as file
    buffer = io.BytesIO()
    buffer.write(msg)
    buffer.seek(0)
    file = discord.File(buffer, filename=filename)
    return file

@bot.event
async def on_ready(): 
    print(f'We are ready to go in {bot.user.name}')
    
@bot.event
async def on_member_join(member: discord.Member): 
    await member.send(f'Welcome to the server, {member.name}')
    
@bot.event
async def on_message(message: discord.Message): 
    if message.author == bot.user: 
        return 
    # if "!clear" in message.content: 
    #     ai.clear_messages()
    #     message.reply("AI message history has been cleared!")
    # elif "!load" in message.content: 
    #     ai.load_messages()
    #     message.reply("AI message history had been loaded!")
    if bot.user in message.mentions: 
        # Send placeholder immediately (prevents timeout)
        thinking = await message.reply(f"{message.author} thinking… 🤔")
        
        try: 
            # Make sure user message is in string format
            user_msg = str(message.content.replace(f"<@{bot.user.id}>", "").strip())
            
            # Store user message
            ai.append_messages(
                "user",
                user_msg
            )

            # Run blocking OpenAI call off the event loop
            await asyncio.to_thread(ai.talk_to_llm)

            messages = ai.get_messages()
            reply: str = messages[-1]["content"]

            # Send response as txt file
            msg = reply.encode("utf-8")
            filename = "respond.txt"
            file = msg_to_file(msg, filename)
            await thinking.delete()
            await message.reply(
                content="Here is your response!",
                file=file
            )
            
        except Exception as e: 
            await thinking.edit(f"Couldn't think of anything, sorry.\n\nERROR: {e}")
    
    await bot.process_commands(message)
    
    
# TODO: Work on functionality so that AI can store convo history
# NOTE: I think that we have to implement github manager to manage file access
# @bot.command()
# async def clear(msg): 
#     ai.clear_messages()
#     await msg.reply("AI chat history has been cleared!")

# @bot.command()
# async def load(msg): 
#     ai.load_messages()
#     await msg.reply("AI chat history had been loaded!")

@bot.command()
async def add_note(msg: discord.Message):
    author = msg.author.mention
    nh.append_notes(author, msg)
    await msg.reply(f"Note added to notes log for {author}")
    
@bot.command()
async def show_notes(msg: discord.Message):
    author = msg.author.mention
    author_notes: dict[str, dict[str, list[str]]] = nh.load_user_notes(author)
    message = ""
    for date in author_notes: 
        message += f"Date: {date}"
        for time in author_notes[date]:
            message += f"\tTime Stamp: {time}"
            notes = author_notes[date].get(time)
            for note in notes: 
                message += f"\t\tNote: {note}"
    file = msg_to_file(message, "notes.txt")
    await msg.reply(
        content=f"Here is your stores notes {author}!",
        file=file
    )    
    

    
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