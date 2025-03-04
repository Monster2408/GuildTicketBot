from discord.ext import commands
from discord import app_commands
from typing import List, AsyncIterator
import discord
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
        await interaction.response.defer(thinking=True, ephemeral=True)
        roles: list = interaction.guild.fetch_roles(name="Ticket Member")
        if roles == None or len(roles) == 0:
            member_role = await interaction.guild.create_role(name="Ticket Member")
        else:
            member_role: discord.Role = roles[0]
        for member in interaction.guild.members:
            if member_role in member.roles:
                continue
            await member.add_roles(member_role)
        await interaction.followup.send("現在サーバー内にいるメンバーを全員サポートメンバーに設定しました。")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(SetRoleCommandCog(bot))