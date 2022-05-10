import discord
import textwrap
import datetime
from discord.ext import commands
from discord import app_commands
from utils.abc import Bot
from typing import List
from utils.functions import getEmojis
from utils.functions import split_message


class Commands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.cached_emojis: dict[int, dict[list, datetime.datetime]] = {}

    @app_commands.command()
    async def test(self, interaction: discord.Interaction):
        """Test command"""
        await interaction.response.send_message("test")

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, text: str):
        """Say something"""
        await interaction.response.send_message("text sent", ephemeral=True)
        await interaction.channel.send(text)

    @app_commands.command()
    @app_commands.rename(emoji_id="emoji")
    async def emojiinfo(self, interaction: discord.Interaction, emoji_id: str):
        """Get information about an emoji"""
        emoji = await interaction.guild.fetch_emoji(emoji_id)
        # emoji_chache = ...
        # emoji_server_data = emoji_cache...
        # discord.utils.get(emoji, [])
        embed = discord.Embed(
            title="Emoji info",
            color=3092790,
        )
        embed.set_thumbnail(url=emoji.url)
        embed.add_field(name="Name", value=emoji.name)
        embed.add_field(name="ID", value=emoji.id)
        embed.add_field(name="Managed", value=emoji.managed)
        if emoji.roles.__len__() > 0:
            embed.add_field(name="Locked to", value=f', '.join(
                str(f"<@&{role.id}>") for role in emoji.roles), inline=False)
        embed.add_field(name="Created at",
                        value=f"<t:{int(emoji.created_at.timestamp())}:D>")
        embed.add_field(name="Uploaded by", value=emoji.user)
        embed.add_field(name="Download link", value=f"[Click here]({emoji.url})")
        await interaction.response.send_message(content=f"`{emoji}`", embed=embed)

    @emojiinfo.autocomplete("emoji_id")
    async def emoji_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        raw_emoji_data = self.cached_emojis.get(interaction.guild_id, {})

        if not raw_emoji_data:
            raw_emojis = await interaction.guild.fetch_emojis()
            self.cached_emojis[interaction.guild_id] = {
                "emojis": raw_emojis,
                "datetime": discord.utils.utcnow(),
            }
        else:
            timeframe = datetime.timedelta(seconds=60*5) # Zeit, wie lange der Cache gültig ist: 5 Minuten
            if raw_emoji_data["datetime"] + timeframe <= discord.utils.utcnow(): # Wenn die Zeit zu lang ist wird der Eintrag gelöscht und neu gefetcht
                self.cached_emojis.pop(interaction.guild_id)
                raw_emojis = await interaction.guild.fetch_emojis()
                self.cached_emojis[interaction.guild_id] = {
                    "emojis": raw_emojis,
                    "datetime": discord.utils.utcnow(),
                }
            else:
                raw_emojis: List[discord.Emoji] = raw_emoji_data["emojis"]

        results = []

        for sub in raw_emojis:
            if all(i in sub.name and sub.name.count(i) >= current.count(i) for i in current):
                results.append(app_commands.Choice(name=sub.name.lower(), value=str(sub.id)))

        return results[0:25]

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def emojis_list(self, interaction: discord.Interaction):
        """List all emojis"""
        guildEmojis = await interaction.guild.fetch_emojis()
        emojiList = '\n'.join(f"{emoji} - `{emoji}`" for emoji in guildEmojis) + \
            f"\n\nLast update: <t:{int(datetime.datetime.timestamp(datetime.datetime.now()))}:D>"
        for content in split_message(emojiList):
            await interaction.channel.send(content=content)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Commands(bot))
