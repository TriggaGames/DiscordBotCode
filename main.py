# Necessary imports
import discord
from discord import app_commands
import io
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import json

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
client = discord.Client(intents=intents) # worry about this later
tree = app_commands.CommandTree(client) # worry about this later
intents.message_content = True
intents.members = True

# Main discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

ai_context = '''
You are an AI agent whos friendly and smart. 
Make sure to provide a Too Long Didn't Read (TL;DR) at the end of your response for big responses, unless your response format cannot allow it or the response does not need a TL;DR.

'''

# Helper bots
ai = AIBot(discord_ai_token, model="gpt-5.2")
ai.append_messages(
    "system",
    ai_context
    )
ai.talk_to_llm()
nh = NotesHandler()

# Helper Functions
def msg_to_file(msg: str, filename: str): 
    buffer = io.BytesIO()
    buffer.write(msg)
    buffer.seek(0)
    file = discord.File(buffer, filename=filename)
    return file
def condense_ai_msg(msg: str, limit: int = 2000) -> list[str]:
    msg = msg.strip()
    
    if (
        msg.startswith("```") or
        (msg.startswith("{") and msg.endswith("}")) or
        (msg.startswith("[") and msg.endswith("]"))
    ):
        return [msg]
    
    chunks = []
    try: 
        paragraphs = msg.split("\n\n")
        for content in paragraphs: 
            content = content.strip()
            
            while len(content) > limit: 
                window = content[:limit]
                
                # Natural sentence breaks
                split_index = -1
                for delimiter in [". ", "! ", "? "]:
                    split_index = window.rfind(delimiter)
                    if split_index != -1:
                        split_index += len(delimiter)
                        break

                if split_index == -1: 
                    split_index = limit
                
                chunks.append(content[:split_index].strip())
                content = content[split_index:].strip()
            
            if content: 
                chunks.append(content)
                
    except Exception: 
        chunks.append(msg)
        
    return chunks

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

            # Send response as structured responses
            responses = condense_ai_msg(reply)
            await thinking.delete()
            for msg in responses: 
                condensed_response = await message.reply(msg)
            
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
async def add_note(ctx: commands.Context, *, note_text: str):
    author = ctx.author.mention
    notes = note_text.splitlines()
    nh.append_notes(author, notes)
    await ctx.reply(f"Note added to notes log for {author}")
    
@bot.command()
async def show_notes(ctx: commands.Context, *, filetype: str):
    author = ctx.author.mention
    author_notes: dict[str, dict[str, list[str]]] = nh.load_user_notes(author)

    valid_types = [".json", ".md", ".txt"]

    filetype = filetype.lower().strip()

    if not filetype.startswith("."):
        filetype = "." + filetype

    if filetype not in valid_types:
        filetype = ".txt"

    filename = f"notes{filetype}"

    if filetype == ".json":
        output = json.dumps(author_notes, indent=4)
    else:
        output = ""
        for date in author_notes:
            output += f"Date: {date}\n"
            for time in author_notes[date]:
                output += f"\tTime Stamp: {time}\n"
                for note in author_notes[date][time]:
                    output += f"\t\tNote: {note}\n"

    file = msg_to_file(output.encode("utf-8"), filename)

    await ctx.reply(
        content=f"Here is your stored notes {author}!",
        file=file
    )

@bot.command()
async def print_ai_message_history(ctx: commands.Context):
    messages = ai.get_messages()
    await ctx.reply(repr(messages))
    
    
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