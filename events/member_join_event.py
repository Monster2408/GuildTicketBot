import discord
from discord import app_commands
from discord.ext import commands
import Var
import traceback
import datetime
from flaretool.holiday import JapaneseHolidays

import database as DB
import function as Func

# import logging
# logging.basicConfig(level=logging.DEBUG)

class MemberJoinClickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'load event cog: {self.__class__.__name__}')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id_list: list = DB.get_support_guild_id_list()
        if len(guild_id_list) == 0:
            return
        for guild_id in guild_id_list:
            guild: discord.Guild = self.bot.get_guild(int(guild_id))
            if guild is None:
                continue
            member_role: discord.Role = discord.utils.get(guild.roles, name=Var.TICKET_MEMBER_ROLE_NAME)
            if member_role == None:
                member_role = await guild.create_role(name=Var.TICKET_MEMBER_ROLE_NAME)
            if member_role not in member.roles:
                DB.set_delete_time(guild.id, 5)
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberJoinClickCog(bot))