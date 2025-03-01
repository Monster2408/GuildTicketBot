# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import locale
locale.setlocale(locale.LC_ALL, '')
from datetime import datetime
import traceback 
import pytz
from japanera import EraDate
import asyncio

import Var, database

DEBUGMODE = False

CMD_COGS = [
    'cmds.panel_cmd',
    'cmds.role_panel_cmd',
    'cmds.rank_cmd',
]

EVENT_COGS = [
    'events.message_event',
    'events.reaction_event',
    'events.voice_state_update_event',
    'events.button_click_event',
]

class MyBot(commands.Bot):
    def __init__(self, prefix: str, intents: discord.Intents):
        database.init()
        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        for cog in CMD_COGS:
            try:
                await self.load_extension(cog)
            except Exception:
                traceback.print_exc()
        for cog in EVENT_COGS:
            try:
                await self.load_extension(cog)
            except Exception:
                traceback.print_exc()
        # スラッシュコマンドの同期をここで実行
        try:
            synced = await self.tree.sync(guild=None)
            print(f"Synced global commands. {synced}")
            for guild in self.guilds:
                synced = await self.tree.sync(guild=discord.Object(id=guild.id))
                print(f"Synced guild command(id={str(guild.id)}). {synced}")
        except Exception:
            traceback.print_exc()  # どこでエラーが発生したか表示

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print(f'{self.user.name}のバージョンはv{Var.BOT_VERSION}')
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        era_date = EraDate(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))
        now = time.strftime(' %H時%M分%S秒')
        print('現在時刻 ' + era_date.strftime("%-E%-O年%m月%d日") + now)
        print(f'{Var.BOT_MODULE}のバージョンはv{discord.__version__}')
        print('-----')
        await self.wait_until_ready()
        await self.change_presence(status=discord.Status.online, activity=discord.Game("/help"))

async def main():
    bot = MyBot(intents=discord.Intents.all(), prefix='!?')
    await bot.start(token=Var.token)

if __name__ == '__main__':
    asyncio.run(main())