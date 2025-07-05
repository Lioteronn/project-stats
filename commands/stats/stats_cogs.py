from typing import Optional

import nextcord
from discord.ext import commands


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="update_info", description="Update the stats for a user."
    )
    async def update_stats(
        self,
        interaction: nextcord.Interaction,
        steam_id: Optional[str] = None,
        steam_url: Optional[str] = None,
    ):
        """Update the stats for a user."""
        if not steam_id and not steam_url:
            await interaction.response.send_message(
                "Please provide a valid Steam ID or URL.",
                ephemeral=True,
            )
