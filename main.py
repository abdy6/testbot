import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
from datetime import timedelta
from math import floor

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

start_time = time.monotonic()

extensions = [
    'testbot_commands'
]

# Check if user is me (adam.2006)
def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 424970840015110145
    return commands.check(predicate)

class TestBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        for ext in extensions:
            await self.load_extension(ext)
            print(f'loaded extension {ext}')
    
    async def on_ready(self):
        print(f'logged in as {self.user}')
        try:
            synced = await self.tree.sync()
            print(f'synced {len(synced)} commands: {[cmd.name for cmd in synced]}')
        except Exception as e:
            print(e)


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
testbot = TestBot(command_prefix=';', intents=intents)

# Debug commands

@testbot.command(name='sync')
@is_me()
async def _sync(ctx, guild: discord.Guild):
    synced = await testbot.tree.sync(guild=guild)
    print(f'synced {len(synced)} commands manually: {[cmd.name for cmd in synced]}')

@testbot.command(name='reload')
@is_me()
async def _reload(ctx, extension: str):
    try:
        await testbot.unload_extension(extension)
        await testbot.load_extension(extension)
    except Exception as e:
        await ctx.send(f'There was an error(`{type(e).__name__}`), check console.')
        print(e)
    else:
        await ctx.send(f'Reloaded extension `{extension}`')

testbot.run(TOKEN)
