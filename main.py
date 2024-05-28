import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime
import time

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

extensions = [
    'testbot_commands'
]

# Check if user is me (adam.2006)
# This is for testing purposes only
def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 424970840015110145
    return commands.check(predicate)

class TestBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

        # Get the start date (for displaying)
        self.start_time = datetime.datetime.now()
        # Used to count the bot's uptime
        self.monotonic_start_time = time.monotonic()

    async def setup_hook(self) -> None:
        # Load all required extensions
        for ext in extensions:
            await self.load_extension(ext)
            print(f'loaded extension {ext}')
    
    async def on_ready(self):
        print(f'logged in as {self.user}')

        # Sync all app commands
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
# Sync commands for guild (doesn't work currently)
@testbot.command(name='sync')
@is_me()
async def _sync(ctx, guild: discord.Guild):
    synced = await testbot.tree.sync(guild=guild)
    print(f'synced {len(synced)} commands manually: {[cmd.name for cmd in synced]}')

# Reload specified module
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
        print(f'reloaded {extension}')

testbot.run(TOKEN)
