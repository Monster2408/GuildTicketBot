from discord.ext import commands, tasks
import discord
import asyncpg

import database as DB
import Var

class taskCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def cog_load(self):
        self.time_check.start()

    async def cog_unload(self):
        self.time_check.cancel()
    
    @tasks.loop(seconds=60)
    async def time_check(self):
        guild_id_list = [int(gid) for gid in DB.get_support_guild_id_list()]
        print(f"guild_id_list: {guild_id_list}")
        for guild_id in guild_id_list:
            print(f"{guild_id} : {type(guild_id)}")
            guild: discord.Guild = await self.bot.fetch_guild(guild_id)
            if guild == None:
                print(f"guild none! guild_id: {guild_id}")
                continue
            print(f"guild_name: {guild.name}")
            count_ok: bool = True
            for vc in guild.voice_channels:
                if len(vc.members) != 0:
                    count_ok = False
                    break
            time = DB.get_delete_time(guild.id)
            if time != -1:
                if count_ok:
                    time -= 1
                    print(f"time: {time}")
                    if time == 0:
                        role: discord.Role = discord.utils.get(guild.roles, name=Var.TICKET_MEMBER_ROLE_NAME)
                        if role == None:
                            role = await guild.create_role(name=Var.TICKET_MEMBER_ROLE_NAME)
                        for member in guild.members:
                            print(member)
                            if role in member.roles:
                                continue
                            await member.kick(reason="チケットサーバーが空いたため退出しました。")
                        DB.set_delete_time(guild.id, -999)
                    else:
                        DB.set_delete_time(guild.id, time)
                else:
                    DB.set_delete_time(guild.id, 5)

async def setup(bot: commands.Bot):
    await bot.add_cog(taskCog(bot))
