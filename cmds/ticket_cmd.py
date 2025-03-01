from discord.ext import commands
from discord import app_commands
from typing import List, AsyncIterator
import discord
import function as Func

class PanelCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
    # テストコマンド
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'load command cog: {self.__class__.__name__}')
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="panel", description="設定用パネルを表示します。")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        view: discord.ui.View = discord.ui.View()
        view.add_item(discord.ui.Button(label="Ticket✉", style=discord.ButtonStyle.primary, custom_id="ticket"))
        await interaction.channel.send(content="Ticketを発行する", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(PanelCommandCog(bot))