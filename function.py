import discord
from discord.ext import commands
import traceback

def select_guild_channel(bot: commands.Bot, inter: discord.Interaction, select_ui_id: str, placeholder: str, page: int = 1, multi_select: int = 1) -> dict:
    try:
        guild_list: list[discord.Guild] = []
        for guild in bot.guilds:
            if guild.get_member(inter.user.id) is not None and inter.guild != guild:
                guild_list.append(guild)
        total_guilds = len(guild_list)
        if multi_select < 1:
            multi_select = 1
        elif multi_select > 25:
            multi_select = 25
        
        if multi_select > total_guilds:
            multi_select = total_guilds
        
        print(f"total_guilds: {total_guilds}")

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