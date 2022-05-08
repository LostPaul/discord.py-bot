import discord
import datetime
from discord.ext import commands
from discord import app_commands
from utils.abc import Bot
from typing import List
from utils.getEmojis import getEmojis


class Commands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        #  self.cached_emojis = dict[int, dict[list, datetime.datetime]] = {}

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
    async def emojiinfo(self, interaction: discord.Interaction, emoji: str):
        """Get info about emoji"""
        emoji = await interaction.guild.fetch_emoji(emoji)
        embed = discord.Embed(
            title="Emoji info",
            color=3092790,
        )
        embed.set_thumbnail(url=emoji.url)
        embed.add_field(name="Name", value=emoji.name)
        embed.add_field(name="ID", value=emoji.id)
        embed.add_field(name="Managed", value=emoji.managed)
        if emoji.roles.__len__() > 0:
            embed.add_field(name="Locked to", value=f', '.join(str(f"<@&{role.id}>") for role in emoji.roles), inline=False)
        embed.add_field(name="Created at", value=f"<t:{int(emoji.created_at.timestamp())}:D>")
        embed.add_field(name="Uploaded by", value=emoji.user)
        embed.add_field(name="Download link", value=f"[Click here]({emoji.url})")
        await interaction.response.send_message(content=f"`{emoji}`",embed=embed)

    @emojiinfo.autocomplete('emoji')
    async def fruits_autocomplete(self, interaction: discord.Interaction, current: str, ) -> List[app_commands.Choice[str]]:
        guildEmojis = await interaction.guild.fetch_emojis()
        if len(getEmojis(current)) > 0:
            return [app_commands.Choice(name=emoji["name"], value=emoji["id"]) for emoji in getEmojis(current) if await interaction.guild.fetch_emoji(emoji["id"]) is not None]
        else:
            return [app_commands.Choice(name=emoji.name, value=str(emoji.id)) for emoji in guildEmojis if current.lower() in emoji.name.lower()][0:25]


async def setup(bot: Bot) -> None:
    await bot.add_cog(Commands(bot))
