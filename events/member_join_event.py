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
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberJoinClickCog(bot))