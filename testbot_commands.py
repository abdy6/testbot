from discord.ext import commands
from discord import app_commands
import discord

# Check if the user is me (adam.2006)
# Testing purposes
def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 424970840015110145
    return commands.check(predicate)

class TestBotCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Just an echo command for testing
    @commands.hybrid_command(name='echo', description='Send the passed string in chat')
    @app_commands.describe(message='What to send')
    @is_me()
    async def echo(self, ctx, *, message: str):
        await ctx.send(message)

    # Take a message link and reply to that message with the passed argument
    @commands.hybrid_command(name='replyto', description='Reply to message in specific channel')
    @app_commands.describe(message_link='link to the message', message='What to send')
    @is_me()
    async def replyto(self, ctx, message_link: str, message: str):
        # Get the message and channel IDs from the link (this is probably a crude way to do it  but it works)
        split_link = message_link.split('/')
        channel_id = int(split_link[-2])
        message_id = int(split_link[-1])

        print(f'channel: {channel_id}, message: {message_id}')

        channel = self.bot.get_channel(channel_id)
        reply_to = await channel.fetch_message(message_id)
        await reply_to.reply(message)
        await ctx.reply("The message was sent", ephemeral=True)

    # Send a message in a specific channel (without reply)
    @commands.hybrid_command(name='say', description='Make the bot say something in a channel. To reply to someone use /replyto.')
    @app_commands.describe(channel='the channel ID to send message in', message='the message to send')
    async def say_msg(self, ctx, channel: int, *, message: str):
        try:
            await self.bot.get_channel(channel).send(message)
        except Exception as e:
            print(e)
            ctx.reply("There was an error, check logs for more info.")
        else:
            print(f'sent msg "{message}" in channel {channel}')


async def setup(bot):
    await bot.add_cog(TestBotCommands(bot=bot))
