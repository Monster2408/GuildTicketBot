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
            print(custom_id)
            print(inter.data)
            if custom_id.startswith("link_guild_"):
                message_id: int = inter.message.id
                await inter.response.defer(thinking=False)
                values: list = inter.data["values"]
                for guild_id in values:
                    DB.link_guild(guild_id, inter.guild.id)
                await inter.followup.edit_message(message_id=message_id, content="サポートサーバーをリンクしました。", view=None)
            elif custom_id.startswith("unlink_guild_"):
                pass
            elif custom_id.startswith("link_guild_next_"):
                page: int = int(custom_id.split("_")[-1])
                data: dict = Func.select_guild_channel(self.bot, inter, "link_guild", "サポートサーバーを選択してください。", page, 25)
                view: discord.ui.View = discord.ui.View()
                view.add_item(data["select_ui"])
                last_page: int = data["last_page"]
                view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="前へ", custom_id="link_guild_prev_" + str(page - 1), disabled=page == 1))
                view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="次へ", custom_id="link_guild_next_" + str(page + 1), disabled=page == last_page))
                await inter.followup.edit_message(content="サポートサーバーを選択してください。", view=view)
            elif custom_id.startswith("link_guild_prev_"):
                page: int = int(custom_id.split("_")[-1])
                data: dict = Func.select_guild_channel(self.bot, inter, "link_guild", "サポートサーバーを選択してください。", page, 25)
                view: discord.ui.View = discord.ui.View()
                view.add_item(data["select_ui"])
                last_page: int = data["last_page"]
                view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="前へ", custom_id="link_guild_prev_" + str(page - 1), disabled=page == 1))
                view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="次へ", custom_id="link_guild_next_" + str(page + 1), disabled=page == last_page))
                await inter.followup.edit_message(content="サポートサーバーを選択してください。", view=view)
        except Exception:
            traceback.print_exc()
        

    async def on_button_click(self, inter:discord.Interaction):
        custom_id: str = inter.data["custom_id"]#inter.dataからcustom_idを取り出す
        if custom_id == "ticket":
            
            await self.ticket(inter)


    async def ticket(self, inter:discord.Interaction):
        try:
            await inter.response.defer(thinking=False, ephemeral=True)
            guild_id_list: list = DB.get_guild_id_list(inter.guild.id)
            if len(guild_id_list) == 0:
                await inter.followup.send("このサーバーには紐づけられたチケットサーバーがありません。", ephemeral=True)
                return
            for guild_id in guild_id_list:
                guild: discord.Guild = self.bot.get_guild(int(guild_id))
                if guild is None:
                    print(f"guild none! guild_id: {guild_id}")
                    continue
                member_role: discord.Role = await Func.create_role(guild)
                if member_role is None:
                    print(f"member_role none! guild_id: {guild_id}")
                    continue
                active_server: bool = False
                for member in guild.members:
                    if member.id == inter.user.id:
                        await inter.followup.send("既にチケットサーバーに参加しています。", ephemeral=True)
                        return
                    if member_role not in member.roles:
                        print(f"has not role: {member.name}")
                        active_server = True
                        break
                invite_url = DB.get_invite_url(inter.user.id, guild.id)
                final_invite_url = None
                for invite in await guild.invites():
                    if final_invite_url is not None:
                        break
                    print(f"invite.url: {invite.url}")
                    print(f"invite_url: {invite_url}")
                    if invite.url == invite_url:
                        final_invite_url = invite_url
                        break
                    if invite.max_uses == 1:
                        active_server = True
                        break
                if final_invite_url:
                    await inter.followup.send(f"{guild.name}に招待します。\n{final_invite_url}", ephemeral=True)
                    return
                if active_server:
                    print(f"active server: {guild.name}")
                    continue
                invite: discord.Invite = await guild.text_channels[0].create_invite(max_uses=1, max_age=60*5)
                DB.update_invite_url(inter.user.id, guild.id, inter.guild.id, invite.url)
                await inter.followup.send(f"{guild.name}に招待します。\n{invite.url}", ephemeral=True)
                return
            await inter.followup.send("このサーバーにはチケットサーバーがありません。", ephemeral=True)
        except Exception:
            traceback.print_exc()
            

async def setup(bot: commands.Bot):
    await bot.add_cog(ButtonClickCog(bot))