import discord

from utils.abc import Bot
from config.config import Token

intents = discord.Intents.default()
intents.guild_messages = True
intents.typing = False

client = Bot("?", intents=intents)


@client.event
async def on_ready():
    client.logger.info(f"Logged in as {client.user.name} ({client.user.id})")


client.run(Token.bot)