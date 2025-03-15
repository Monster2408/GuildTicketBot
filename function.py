import discord
from discord.ext import commands
import traceback

import Var
import database as DB

def select_guild_channel(bot: commands.Bot, inter: discord.Interaction, select_ui_id: str, placeholder: str, page: int = 1, multi_select: int = 1) -> dict:
    try:
        guild_list: list[discord.Guild] = []
        guild_id_list: list = DB.get_guild_id_list(inter.guild.id)
        print(guild_id_list)
        for guild in bot.guilds:
            if guild.get_member(inter.user.id) is not None and inter.guild != guild:
                if select_ui_id == "link_guild":
                    if str(guild.id) not in guild_id_list:
                        print(f"if guild.id not in guild_id_list: {guild.name}")
                        guild_list.append(guild)
                elif select_ui_id == "unlink_guild":
                    if str(guild.id) in guild_id_list:
                        print(f"if guild.id in guild_id_list: {guild.name}")
                        guild_list.append(guild)
                else:
                    guild_list.append(guild)
        total_guilds = len(guild_list)
        if multi_select < 1:
            multi_select = 1
        elif multi_select > 25:
            multi_select = 25
        
        if multi_select > total_guilds:
            multi_select = total_guilds

        # 1ページあたりの項目数
        items_per_page = 25

        # ページの範囲を計算
        start = items_per_page * (page - 1)
        end = items_per_page * page

        last_page = page
        # 範囲外なら最後のページを選ぶ
        if start >= total_guilds:
            last_page = (total_guilds // items_per_page) + (1 if total_guilds % items_per_page else 0)
            start = items_per_page * (last_page - 1)
            end = total_guilds  # 最後のページはリストの終端まで
            page = last_page

        options = []
        for guild in guild_list[start:end]:
            options.append(discord.SelectOption(label=guild.name, value=str(guild.id)))

        select_ui = discord.ui.Select(custom_id=select_ui_id + "_" + str(page), placeholder=placeholder, options=options, max_values=multi_select)
        return {"select_ui": select_ui, "page": page, "last_page": last_page}
    except Exception:
        traceback.print_exc()
        return {"select_ui": None, "page": 1, "last_page": 1}

async def create_role(guild: discord.Guild) -> discord.Role:
    role: discord.Role = discord.utils.get(guild.roles, name=Var.TICKET_MEMBER_ROLE_NAME)
    if role == None:
        role = await guild.create_role(name=Var.TICKET_MEMBER_ROLE_NAME)
    roles = guild.roles  # 全ロール取得
    await role.edit(position=roles[-2].position)  # 一番下のロールの位置に設定
    return role