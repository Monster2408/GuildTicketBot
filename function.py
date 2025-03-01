import discord
from discord.ext import commands
import traceback

def select_text_channel(guild: discord.Guild, select_ui_id: str, placeholder: str, page: int = 1) -> dict:
    text_channel_list = guild.text_channels
    total_channels = len(text_channel_list)

    # 1ページあたりの項目数
    items_per_page = 25

    # ページの範囲を計算
    start = items_per_page * (page - 1)
    end = items_per_page * page

    last_page = page
    # 範囲外なら最後のページを選ぶ
    if start >= total_channels:
        last_page = (total_channels // items_per_page) + (1 if total_channels % items_per_page else 0)
        start = items_per_page * (last_page - 1)
        end = total_channels  # 最後のページはリストの終端まで
        page = last_page

    options = []
    for text_channel in text_channel_list[start:end]:
        category_name: str = f"({text_channel.category.name})" if text_channel.category is not None else ""
        options.append(discord.SelectOption(label="#"+text_channel.name+category_name, value=str(text_channel.id)))

    select_ui = discord.ui.Select(custom_id=select_ui_id + "_" + str(page), placeholder=placeholder, options=options)
    return {"select_ui": select_ui, "page": page, "last_page": last_page}

def select_vc_channel(guild: discord.Guild, select_ui_id: str, placeholder: str, page: int = 1) -> dict:
    vc_channel_list = guild.voice_channels
    total_channels = len(vc_channel_list)

    # 1ページあたりの項目数
    items_per_page = 25

    # ページの範囲を計算
    start = items_per_page * (page - 1)
    end = items_per_page * page

    last_page = page
    # 範囲外なら最後のページを選ぶ
    if start >= total_channels:
        last_page = (total_channels // items_per_page) + (1 if total_channels % items_per_page else 0)
        start = items_per_page * (last_page - 1)
        end = total_channels  # 最後のページはリストの終端まで
        page = last_page
    options = []
    for vc_channel in vc_channel_list[start:end]:
        category_name: str = f"({vc_channel.category.name})" if vc_channel.category is not None else ""
        options.append(discord.SelectOption(label="🔈"+vc_channel.name+category_name, value=str(vc_channel.id)))

    select_ui = discord.ui.Select(custom_id=select_ui_id + "_" + str(page), placeholder=placeholder, options=options)
    return {"select_ui": select_ui, "page": page, "last_page": last_page}

def select_role(guild: discord.Guild, select_ui_id: str, placeholder: str, page: int = 1) -> dict:
    role_list = guild.roles
    total_roles = len(role_list)

    # 1ページあたりの項目数
    items_per_page = 25

    # ページの範囲を計算
    start = items_per_page * (page - 1)
    end = items_per_page * page

    last_page = page
    # 範囲外なら最後のページを選ぶ
    if start >= total_roles:
        last_page = (total_roles // items_per_page) + (1 if total_roles % items_per_page else 0)
        start = items_per_page * (last_page - 1)
        end = total_roles  # 最後のページはリストの終端まで
        page = last_page

    options = [
        discord.SelectOption(label=role.name, value=str(role.id))
        for role in role_list[start:end]
    ]

    select_ui = discord.ui.Select(custom_id=select_ui_id + "_" + str(page), placeholder=placeholder, options=options)
    return {"select_ui": select_ui, "page": page, "last_page": last_page}

def get_panel_embed(bot: commands.bot) -> discord.Embed:
    embed: discord.Embed = discord.Embed(title="どの設定を変更しますか？", description="", color=0x00bfff)
    embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar.url)
    #embed.add_field(name="ランキングシステム", value="未実装", inline=False)
    embed.add_field(name="VCプロフィール機能", value="🚷 除外VC設定\n📚 ﾌﾟﾛﾌｨｰﾙﾁｬﾝﾈﾙ設定", inline=False)
    #embed.add_field(name="ﾀｲﾑｱｳﾄ", value="⌚ ﾀｲﾑｱｳﾄ通知ﾁｬﾝﾈﾙ設定", inline=False)
    embed.add_field(name="パネル更新", value="🔄 パネル更新", inline=False)
    return embed

def get_panel_view() -> discord.ui.View:
    view: discord.ui.View = discord.ui.View()
    vc_profile_exclusion_vc_button: discord.ui.Button = discord.ui.Button(style=discord.ButtonStyle.green, label="🚷", custom_id="vc_profile_exclusion_vc")
    view.add_item(vc_profile_exclusion_vc_button)
    vc_profile_setting_channel_button: discord.ui.Button = discord.ui.Button(style=discord.ButtonStyle.green, label="📚", custom_id="vc_profile_setting_channel")
    view.add_item(vc_profile_setting_channel_button)
    timeout_notice_channel_button: discord.ui.Button = discord.ui.Button(style=discord.ButtonStyle.green, label="⌚", custom_id="timeout_notice_channel")
    #view.add_item(timeout_notice_channel_button)
    rank_system_button: discord.ui.Button = discord.ui.Button(style=discord.ButtonStyle.green, label="📊", custom_id="rank_system")
    view.add_item(rank_system_button)
    refresh_button: discord.ui.Button = discord.ui.Button(style=discord.ButtonStyle.green, label="🔄", custom_id="refresh")
    view.add_item(refresh_button)
    return view

async def send_role_panel_embed(
    interaction: discord.Interaction,
    bot: commands.bot, 
    title: str,
    single: str, 
    role_a: discord.Role, 
    description: str = None, 
    role_b: discord.Role = None, 
    role_c: discord.Role = None, 
    role_d: discord.Role = None, 
    role_e: discord.Role = None, 
    role_f: discord.Role = None, 
    role_g: discord.Role = None, 
    role_h: discord.Role = None, 
    role_i: discord.Role = None, 
    role_j: discord.Role = None, 
    role_k: discord.Role = None, 
    role_l: discord.Role = None, 
    role_m: discord.Role = None, 
    role_n: discord.Role = None, 
    role_o: discord.Role = None, 
    role_p: discord.Role = None, 
    role_q: discord.Role = None, 
    role_r: discord.Role = None, 
    role_s: discord.Role = None, 
    role_t: discord.Role = None, 
    role_u: discord.Role = None, 
    role_v: discord.Role = None, 
    role_w: discord.Role = None
    ):
    embed: discord.Embed = discord.Embed(title=description, description="※「インタラクションに失敗しました」と表示された場合は不具合が発生しています。<@774615474642223144>に連絡ください。", color=0x00bfff)
    embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar.url)
    view: discord.ui.View = discord.ui.View()
    text: str = f"🇦:{role_a.mention}"
    try:
        view.add_item(discord.ui.Button(emoji="🇦", custom_id="hs_role_a", style=discord.ButtonStyle.green))
        if role_b is not None:
            text += f"\n🇧:{role_b.mention}"
            view.add_item(discord.ui.Button(emoji="🇧", custom_id="hs_role_b", style=discord.ButtonStyle.green))
        if role_c is not None:
            text += f"\n🇨:{role_c.mention}"
            view.add_item(discord.ui.Button(emoji="🇨", custom_id="hs_role_c", style=discord.ButtonStyle.green))
        if role_d is not None:
            text += f"\n🇩:{role_d.mention}"
            view.add_item(discord.ui.Button(emoji="🇩", custom_id="hs_role_d", style=discord.ButtonStyle.green))
        if role_e is not None:
            text += f"\n🇪:{role_e.mention}"
            view.add_item(discord.ui.Button(emoji="🇪", custom_id="hs_role_e", style=discord.ButtonStyle.green))
        if role_f is not None:
            text += f"\n🇫:{role_f.mention}"
            view.add_item(discord.ui.Button(emoji="🇫", custom_id="hs_role_f", style=discord.ButtonStyle.green))
        if role_g is not None:
            text += f"\n🇬:{role_g.mention}"
            view.add_item(discord.ui.Button(emoji="🇬", custom_id="hs_role_g", style=discord.ButtonStyle.green))
        if role_h is not None:
            text += f"\n🇭:{role_h.mention}"
            view.add_item(discord.ui.Button(emoji="🇭", custom_id="hs_role_h", style=discord.ButtonStyle.green))
        if role_i is not None:
            text += f"\n🇮:{role_i.mention}"
            view.add_item(discord.ui.Button(emoji="🇮", custom_id="hs_role_i", style=discord.ButtonStyle.green))
        if role_j is not None:
            text += f"\n🇯:{role_j.mention}"
            view.add_item(discord.ui.Button(emoji="🇯", custom_id="hs_role_j", style=discord.ButtonStyle.green))
        if role_k is not None:
            text += f"\n🇰:{role_k.mention}"
            view.add_item(discord.ui.Button(emoji="🇰", custom_id="hs_role_k", style=discord.ButtonStyle.green))
        if role_l is not None:
            text += f"\n🇱:{role_l.mention}"
            view.add_item(discord.ui.Button(emoji="🇱", custom_id="hs_role_l", style=discord.ButtonStyle.green))
        if role_m is not None:
            text += f"\n🇲:{role_m.mention}"
            view.add_item(discord.ui.Button(emoji="🇲", custom_id="hs_role_m", style=discord.ButtonStyle.green))
        if role_n is not None:
            text += f"\n🇳:{role_n.mention}"
            view.add_item(discord.ui.Button(emoji="🇳", custom_id="hs_role_n", style=discord.ButtonStyle.green))
        if role_o is not None:
            text += f"\n🇴:{role_o.mention}"
            view.add_item(discord.ui.Button(emoji="🇴", custom_id="hs_role_o", style=discord.ButtonStyle.green))
        if role_p is not None:
            text += f"\n🇵:{role_p.mention}"
            view.add_item(discord.ui.Button(emoji="🇵", custom_id="hs_role_p", style=discord.ButtonStyle.green))
        if role_q is not None:
            text += f"\n🇶:{role_q.mention}"
            view.add_item(discord.ui.Button(emoji="🇶", custom_id="hs_role_q", style=discord.ButtonStyle.green))
        if role_r is not None:
            text += f"\n🇷:{role_r.mention}"
            view.add_item(discord.ui.Button(emoji="🇷", custom_id="hs_role_r", style=discord.ButtonStyle.green))
        if role_s is not None:
            text += f"\n🇸:{role_s.mention}"
            view.add_item(discord.ui.Button(emoji="🇸", custom_id="hs_role_s", style=discord.ButtonStyle.green))
        if role_t is not None:
            text += f"\n🇹:{role_t.mention}"
            view.add_item(discord.ui.Button(emoji="🇹", custom_id="hs_role_t", style=discord.ButtonStyle.green))
        if role_u is not None:
            text += f"\n🇺:{role_u.mention}"
            view.add_item(discord.ui.Button(emoji="🇺", custom_id="hs_role_u", style=discord.ButtonStyle.green))
        if role_v is not None:
            text += f"\n🇻:{role_v.mention}"
            view.add_item(discord.ui.Button(emoji="🇻", custom_id="hs_role_v", style=discord.ButtonStyle.green))
        embed.add_field(name="役職パネル", value=text, inline=False)
        embed.add_field(name="重複許可", value=single, inline=False)
        await interaction.response.send_message(embed=embed, view=view)
    except Exception:
        traceback.print_exc()  # どこでエラーが発生したか表示
        await interaction.response.send_message(content="インタラクションに失敗しました。", ephemeral=True)

select_role_panel: dict = {}

def add_select_role_panel(user_id: int, message_id: int):
    global select_role_panel
    select_role_panel[user_id] = message_id

def get_select_role_panel(user_id: int) -> int:
    global select_role_panel
    return select_role_panel[user_id]