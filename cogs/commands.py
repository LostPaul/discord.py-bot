import discord
from discord.ext import commands
from discord import app_commands
from utils.abc import Bot
from typing import List
from utils.getEmojis import getEmojis

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
    async def fruits(self, interaction: discord.Interaction, fruits: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruits}')

    @fruits.autocomplete('fruits')
    async def fruits_autocomplete(self, interaction: discord.Interaction, current: str, ) -> List[app_commands.Choice[str]]:
        guildEmojis = await interaction.guild.fetch_emojis()
        if len(getEmojis(current)) > 0:
            return [app_commands.Choice(name=emoji["name"], value=emoji["id"]) for emoji in getEmojis(current) if await interaction.guild.fetch_emoji(emoji["id"]) is not None]
        else:
            return [app_commands.Choice(name=emoji.name, value=str(emoji.id)) for emoji in guildEmojis if current.lower() in emoji.name.lower() ][0:25]


async def setup(bot: Bot) -> None:
    await bot.add_cog(Commands(bot))
