from discord.ext import commands
from discord import app_commands
from typing import List, AsyncIterator
import discord
import function as Func

class LinkGuildCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
    # テストコマンド
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'load command cog: {self.__class__.__name__}')
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="link_guild", description="サポートサーバーをリンクします。")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        data: dict = Func.select_guild_channel(self.bot, interaction.user, "link_guild", "サポートサーバーを選択してください。")
        view: discord.ui.View = discord.ui.View()
        view.add_item(data["select_ui"])
        await interaction.followup.send("サポートサーバーを選択してください。", view=view)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(LinkGuildCommandCog(bot))