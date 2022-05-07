import discord

from utils.abc import Bot
from config.config import Token

intents = discord.Intents.default()
intents.typing = False

bot = Bot("?", intents=intents)


@bot.event
async def on_ready():
    bot.logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")


bot.run(Token.bot)