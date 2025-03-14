from discord.ext import commands, tasks
import discord
import traceback

import database as DB
import function as Func

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
        print("==========")
        print(guild_id_list)
        print("==========")
        for guild_id in guild_id_list:
            print(f"{guild_id} : {type(guild_id)}")
            guild: discord.Guild = await self.bot.fetch_guild(guild_id)
            if guild == None:
                print(f"guild none! guild_id: {guild_id}")
                continue
            count_ok: bool = True
            member_role: discord.Role = await Func.create_role(guild)
            if member_role is None:
                print(f"member_role none! guild_id: {guild_id}")
                continue
            async for member in guild.fetch_members(limit=None):
                if member_role in member.roles:
                    continue
                print(f"{member.name} : {member.voice}")
                if member.voice == None:
                    continue
                if member.voice.channel != None:
                    count_ok = False
                    break
            time = DB.get_delete_time(guild.id)
            if time != -1:
                if count_ok:
                    time -= 1
                    if time == 0:
                        async for member in guild.fetch_members(limit=None):
                            if member_role in member.roles:
                                continue
                            await member.kick(reason="チケットサーバーが空いたため退出しました。")
                        DB.set_delete_time(guild.id, -999)
                    else:
                        DB.set_delete_time(guild.id, time)
                else:
                    DB.set_delete_time(guild.id, 5)

async def setup(bot: commands.Bot):
    await bot.add_cog(taskCog(bot))
