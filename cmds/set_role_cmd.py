from discord.ext import commands
from discord import app_commands
from typing import List, AsyncIterator
import discord
import traceback


import function as Func

class SetRoleCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
    # テストコマンド
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'load command cog: {self.__class__.__name__}')
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="set_role", description="現在サーバー内にいるメンバーをサポートメンバーに設定します。")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True, ephemeral=True)
            member_role: discord.Role = await Func.create_role(interaction.guild)
            if member_role is None:
                print(f"member_role none! guild_id: {interaction.guild.id}")
                return
            for member in interaction.guild.members:
                if member_role in member.roles:
                    continue
                await member.add_roles(member_role)
            await interaction.followup.send("現在サーバー内にいるメンバーを全員サポートメンバーに設定しました。")
        except Exception:
            traceback.print_exc()
        
async def setup(bot: commands.Bot):
    await bot.add_cog(SetRoleCommandCog(bot))