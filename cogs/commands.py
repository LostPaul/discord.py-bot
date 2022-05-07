import discord
from discord.ext import commands
from discord import app_commands
from utils.abc import Bot
from typing import List


class Commands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def test(self, itx: discord.Interaction):
        """Test command"""
        await itx.response.send_message("test")

    @app_commands.command()
    async def say(self, itx: discord.Interaction, text: str):
        """Say something"""
        await itx.response.send_message("text sent", ephemeral=True)
        await itx.channel.send(text)

    @app_commands.command()
    async def fruits(interaction: discord.Interaction, fruits: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruits}')

    @fruits.autocomplete('fruits')
    async def fruits_autocomplete( 
        interaction: discord.Interaction,
        current: str, 
    ) -> List[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]


async def setup(bot: Bot) -> None:
    await bot.add_cog(Commands(bot))
