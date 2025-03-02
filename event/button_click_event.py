import discord
from discord import app_commands
from discord.ext import commands
import Var
import traceback
import datetime
from flaretool.holiday import JapaneseHolidays

import database as DB

# import logging
# logging.basicConfig(level=logging.DEBUG)

class ButtonClickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    # コグアンロード処理
    def cog_unload(self):
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        print('load event cog: ButtonClickCog')
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_interaction(self, inter:discord.Interaction):
        try:
            if inter.data['component_type'] == 2:
                await self.on_button_click(inter)
            elif inter.data['component_type'] == 3:
                await self.on_select_option(inter)
        except KeyError:
            pass
        
    async def on_select_option(self, inter:discord.Interaction):
        try:
            custom_id: str = inter.data["custom_id"]#inter.dataからcustom_idを取り出す
        except Exception:
            traceback.print_exc()
        

    async def on_button_click(self, inter:discord.Interaction):
        custom_id: str = inter.data["custom_id"]#inter.dataからcustom_idを取り出す
        if custom_id == "ticket":
            await self.ticket(inter)

    async def ticket(self, inter:discord.Interaction):
        await inter.response.defer(thinking=False, ephemeral=True)
        guild_id_list: list = DB.get_guild_id_list(inter.guild.id)
        if len(guild_id_list) == 0:
            await inter.followup.send("このサーバーには紐づけられたチケットサーバーがありません。", ephemeral=True)
            return
        for guild_id in guild_id_list:
            guild: discord.Guild = self.bot.get_guild(int(guild_id))
            if guild is None:
                continue
            roles: list = guild.fetch_roles(name="Ticket Member")
            if len(roles) == 0:
                continue
            member_role: discord.Role = roles[0]
            if member_role is None:
                continue
            

async def setup(bot: commands.Bot):
    await bot.add_cog(ButtonClickCog(bot))