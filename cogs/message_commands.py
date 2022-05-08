import discord
import datetime
from discord.ext import commands
from discord import app_commands
from utils.abc import Bot
from utils.functions import getEmojis


class message_commands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @commands.command()
    async def test(self, ctx, arg):
        """Test command"""
        print("test")
        await ctx.reply("test")


async def setup(bot: Bot) -> None:
    await bot.add_cog(message_commands(bot))
