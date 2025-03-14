from discord.ext import commands
from discord import app_commands
from typing import List, AsyncIterator
import discord
import traceback

import function as Func

class UnlinkGuildCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
    # テストコマンド
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'load command cog: {self.__class__.__name__}')
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="unlink_guild", description="サポートサーバーをリンクします。")
    @app_commands.checks.has_permissions(administrator=True)
    async def unlink_guild(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True, ephemeral=True)
            # TODO: 登録済みの鯖のみ表示したい
            data: dict = Func.select_guild_channel(self.bot, interaction, "unlink_guild", "サポートサーバーを選択してください。", 1, 25)
            view: discord.ui.View = discord.ui.View()
            view.add_item(data["select_ui"])
            last_page: int = data["last_page"]
            page: int = data["page"]
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="前へ", custom_id="unlink_guild_prev_" + str(page - 1), disabled=page == 1))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="次へ", custom_id="unlink_guild_next_" + str(page + 1), disabled=page == last_page))
            await interaction.response.send_message(content="サポートサーバーを選択してください。", view=view, ephemeral=True)
        except Exception:
            traceback.print_exc()
        
async def setup(bot: commands.Bot):
    await bot.add_cog(UnlinkGuildCommandCog(bot))