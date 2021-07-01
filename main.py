import copy
import ssl, msgpack, asyncio, discord, json, sys
import time, datetime, os, threading, requests, shutil, psutil
from prettytable import PrettyTable
from discord.ext import commands
from discord.ext.commands import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageSequence
from io import BytesIO

print("Starting")
uri = "wss://social.krunker.io/ws"
a_headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    "Host": "krunker_social.krunker.io",
    "Origin": "https://krunker.io",
    'Pragma': 'no-cache',
    'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}
bot = commands.Bot(command_prefix=["cw"+" ", "Cw"+" ", "cW"+" ","CW"+" ", "V.", "v."], case_insensitive=True)
bot.remove_command("help")
color = 7929797
sampfp = "https://media.discordapp.net/attachments/854008993248051230/854708889059852288/sam_av.png"
bot.refr = {}
bot.links = {}
bot.data = {}
bot.userdata = {}
bot.bgdata = {}
bot.unsaved = {}
bot.already = []
bot.vntapeeps = []
bot.excl = [671436261482823763]
bot.dcmds = []
bot.dev = ""
economyerror = "❌"
economysuccess = "✅"
disregarded = []
warn1 = []
warn2 = []
devs = [771601176155783198]
usercmds = {}
error_embed = 16730441
embedcolor = 5046208
success_embed = 5963593
bot.uptime = time.time()
bot.reqs = 0
bot.pause = False
bot.cwpause = True
bot.beta = False

bot.help_json = {
    "Wars": {
      "category": "Wars",
      "v.view": {
        "aliases": [
          "None"
        ],
        "usage": "v.view",
        "desc": "Shows wars in embed form"
      },
    "v.end": {
        "aliases": ["None"],
        "usage": "v.end",
        "desc": "Shows estimated war kills of everyone in embed form"
    },
    "v.contract":{
        "aliases":["con"],
        "usage":"v.contract [ign]",
        "desc":"Shows clan wars contract"
    }
    }, "Profile":{
        "category":"Profile",
        "v.profile":{
            "aliases":["p", "pf"],
            "usage":"v.profile [ign]",
            "desc":"Shows profile"
        },
        "v.link":{
            "aliases":["None"],
            "usage":"v.link [ign]",
            "desc":"Links your account to bot"
        },
        "v.pbg":{
            "aliases":["None"],
            "usage":"v.pbg",
            "desc":"Customize your background"
        },
        "v.main":{
            "aliases":["None"],
            "usage":"v.main <ign>",
            "desc":"Sets that account as your main account"
        },
        "v.alts":{
            "aliases":["None"],
            "usage":"v.alts",
            "desc":"View all linked accounts"
        }
    }
}

@bot.check
async def if_allowed(ctx):
    return await check_channel(ctx.channel.id)

@bot.check
async def if_enabled(ctx):
    if ctx.command.name in bot.dcmds:
        await ctx.reply("Command disabled at the moment. Please retry later")
        return False
    else:
        return True

async def check_channel(chlid):
    server = await get_admin()
    if server is None: return True
    if len(server) == 0: return True
    if chlid in server: return True
    else: return False

async def getdata(clan):
    """ssl_context = ssl._create_unverified_context()
                async with websockets.connect(uri=uri, extra_headers=a_headers, ssl=ssl_context) as websocket:
                    data = msgpack.packb(["r", "clanwars", "Q", None, None, None, "0", None], use_bin_type=True) + b"\x00\x00"
                    await websocket.send(data)
                    while True:
                        response_data = msgpack.unpackb((await websocket.recv())[0:-2], raw=False)
                        if response_data[0] == "news": continue
                        elif response_data == ["cpt"]:
                            await bot.get_channel(854008993248051230).send("<@771601176155783198> Captcha")
                            return "retry"
                        elif response_data != ["pi"]: break
                    return response_data"""
    bot.reqs += 1
    #return [{'username': 'HiddenName', 'score': 7081125, 'score7': 999995, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'AlricTheEpic', 'score': 8432135, 'score7': 521690, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'prokillmaster', 'score': 9127628, 'score7': 508650, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': '_Jimmyy_', 'score': 7878985, 'score7': 445520, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'timcuck', 'score': 1044825, 'score7': 403480, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 1, 'timeplayed': 1998827, 'kills': 366, 'deaths': 97, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': '(SoundWave)', 'score': 9682644, 'score7': 374430, 'role': 2, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'HypnoticCandy', 'score': 6188440, 'score7': 318305, 'role': 0, 'hacker': False, 'verified': True, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'PrimePanda', 'score': 18311098, 'score7': 317225, 'role': 1, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'giude', 'score': 6177730, 'score7': 315240, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 1, 'timeplayed': 3658672, 'kills': 618, 'deaths': 204, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': 'flxso', 'score': 8862620, 'score7': 305930, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'TTVHeyItzRiley', 'score': 2481215, 'score7': 299635, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'DinoDS', 'score': 8226703, 'score7': 283100, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'wermiliusgamYT', 'score': 7107445, 'score7': 263760, 'role': 1, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 1, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': '2hsjkddfuh', 'score': 8378255, 'score7': 257260, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'PUNKIN_04', 'score': 6422515, 'score7': 236030, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'FistWiTheWrist', 'score': 1141455, 'score7': 235435, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Tamas601', 'score': 15981120, 'score7': 222790, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'sec_aimboter', 'score': 3493655, 'score7': 221270, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 1, 'timeplayed': 1479929, 'kills': 262, 'deaths': 86, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': 'Berox', 'score': 5850915, 'score7': 211560, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'PigBoss3232', 'score': 6429266, 'score7': 205960, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'TZYellowNugget', 'score': 15179805, 'score7': 201465, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'SK-_-GAMING', 'score': 4769387, 'score7': 197205, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'bathwater-_-', 'score': 10748014, 'score7': 196580, 'role': 2, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Siyamnur', 'score': 8692415, 'score7': 195095, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'The_Vantablack', 'score': 9019388, 'score7': 186040, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'vidgamer', 'score': 14085171, 'score7': 182735, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'alok87', 'score': 30960605, 'score7': 176465, 'role': 1, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'snipereliot', 'score': 15638609, 'score7': 171565, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'JustZorrox', 'score': 12925065, 'score7': 167865, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Nanogun', 'score': 7244465, 'score7': 155870, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'ER7_SQUAD1', 'score': 3673110, 'score7': 142710, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'TTV_Plasma', 'score': 5305595, 'score7': 140080, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'trashplayer187', 'score': 16478290, 'score7': 131420, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'SushiMan69', 'score': 5501001, 'score7': 129640, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'arya4', 'score': 5231335, 'score7': 124430, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 1, 'timeplayed': 746255, 'kills': 141, 'deaths': 45, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': 'PURPLEMUSHROOM', 'score': 8053992, 'score7': 124400, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'K4lt', 'score': 539340, 'score7': 123645, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'MultexGamingYT', 'score': 6771700, 'score7': 119425, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'TeraIO', 'score': 10179749, 'score7': 113475, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'ursociallife2', 'score': 7556087, 'score7': 109135, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'rdhanekula', 'score': 10756897, 'score7': 99725, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'KingWasp', 'score': 5066625, 'score7': 94235, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'xeinny', 'score': 8190260, 'score7': 86540, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Kvb3k', 'score': 7852307, 'score7': 82150, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Urenda06', 'score': 8003970, 'score7': 76770, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': '_68_', 'score': 1433113, 'score7': 76290, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'DragonOfWar', 'score': 5138628, 'score7': 68410, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'forportillo', 'score': 6564425, 'score7': 54545, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Cattiest97', 'score': 8490570, 'score7': 47630, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'FAZEFIREDOES', 'score': 5549176, 'score7': 43290, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'realAffixx', 'score': 7414160, 'score7': 41785, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'TamedKR', 'score': 5606490, 'score7': 39335, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': '0rion86_TOP', 'score': 2817440, 'score7': 36465, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'jacob8793', 'score': 8109249, 'score7': 33200, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'ScopezzUK', 'score': 824215, 'score7': 32900, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'AwesomeSam', 'score': 9288930, 'score7': 27205, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'crzyjo3_ttv', 'score': 3123295, 'score7': 24790, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'JustHaven', 'score': 2387295, 'score7': 19650, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'lmao_epic', 'score': 1167860, 'score7': 17920, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Sklasher20192', 'score': 6906060, 'score7': 17220, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'ensonananyani', 'score': 13218652, 'score7': 16390, 'role': 2, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'IM-aa-boT', 'score': 5439856, 'score7': 15075, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Levinho_', 'score': 3201695, 'score7': 10525, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'minowskii', 'score': 2632935, 'score7': 9430, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 1, 'timeplayed': 562233, 'kills': 123, 'deaths': 19, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': 'helloMods', 'score': 5640530, 'score7': 7390, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'VG-LAGZE', 'score': 13050990, 'score7': 6600, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'yuvijo', 'score': 2019455, 'score7': 5705, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Boomer_Kun', 'score': 4228680, 'score7': 5620, 'role': 1, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'datoneguy123', 'score': 9988505, 'score7': 3765, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'pj06', 'score': 3810741, 'score7': 3125, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'GetR3kt17', 'score': 8844970, 'score7': 2725, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'serpentsnlper', 'score': 3851410, 'score7': 1250, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'HikoyyLeRetour', 'score': 5446630, 'score7': 385, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'aflawedmind', 'score': 3365885, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'jstn_361', 'score': 6543900, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': '-slugy', 'score': 919145, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Gamenight', 'score': 4334450, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Gamer_Zares', 'score': 1140587, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Zebbzter01', 'score': 3065280, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'tornn', 'score': 1601925, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'NISEgfx', 'score': 600030, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'KleinSeuntjie', 'score': 4382045, 'score7': 0, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'aabir(FaZe)', 'score': 5410440, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'imsorrycynthia', 'score': 477875, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'FanaticalRoute', 'score': 3050465, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Symphonyyy', 'score': 1348275, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Kaltein', 'score': 11207890, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'mach6', 'score': 277270, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 1, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 7}, 'clanRank': 6, 'pr': 0}, {'username': 'isilac', 'score': 8927460, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'RyzeAu', 'score': 4233915, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Rand0m_12', 'score': 1709180, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'CITYCREEK', 'score': 753995, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'Melvinthepro', 'score': 9218012, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'HenLee1801', 'score': 5794325, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': True, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'WolfTamer69', 'score': 1620315, 'score7': 0, 'role': 1, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}, {'username': 'shewto', 'score': 2462880, 'score7': 0, 'role': 0, 'hacker': False, 'verified': False, 'premium': False, 'contract': {'state': 0, 'timeplayed': 0, 'kills': 0, 'deaths': 0, 'region': 0}, 'clanRank': 6, 'pr': 0}]
    data = requests.get(f"https://kr.vercel.app/api/clan?clan={clan}")
    res = json.loads(data.text)
    today = bot.data.get(time.strftime("%d-%m-%Y"), {})
    today[res["data"]["name"]] = res
    bot.data[time.strftime("%d-%m-%Y")] = today
    return res

async def embed_view(clan):
    data = await getdata(clan)
    data = data["data"]["members"]
    active = PrettyTable()
    active.field_names = ["Player Name", "Kills", "Deaths", "Time Played"]

    expired = PrettyTable()
    expired.field_names = ["Player Name", "Kills", "Deaths", "Time Played"]

    act = 1
    exp = 1
    activefinal = PrettyTable()
    activefinal.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    expiredfinal = PrettyTable()
    expiredfinal.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]
    allkills = 0
    ellkills = 0
    for i in data:
        j = i
        i = i["contract"]
        timeplayed = int(i["timeplayed"] / 1000)
        left = datetime.timedelta(seconds=timeplayed)
        final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
        colon_format = str(final).split(" ")[1].split(':')

        if timeplayed < 10800 and timeplayed != 0:
            active.add_row([j["username"], i["kills"], i["deaths"],
                            f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            allkills += i["kills"]

        elif timeplayed >= 10800:
            expired.add_row([j["username"], i["kills"], i["deaths"],
                             f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            ellkills += i["kills"]
    activefinal.title = f"Active Contracts- {allkills} kills"
    expiredfinal.title = f"Expired Contracts- {ellkills} kills"
    active.sortby = "Kills"
    active.reversesort = True
    finallist = []
    for i in active._rows:
        finallist.append(i[1])
    finallist.sort(reverse=True)
    for i in range(1, len(finallist) + 1):
        for j in active._rows:
            if j[1] == finallist[i-1]:
                mylist = j
                mylist.insert(0, f"{i}.")
                activefinal.add_row(mylist)
    del active
    active = activefinal
    actlist = []
    explist = []

    count = 0
    while True:
        if len(active.get_string()) <= 2000:
            active_con = discord.Embed(description=f"```css\n{active}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            actlist.append(active_con)
            break
        else:
            if count > len(active.get_string()): break
            active_con = discord.Embed(description=f"```css\n{active.get_string()[count:2000]}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            count += 2000
            actlist.append(active_con)

    expired.sortby = "Kills"
    expired.reversesort = True
    finallist = []
    for i in expired._rows:
        finallist.append(i[1])
    finallist.sort(reverse=True)
    for i in range(1, len(finallist) + 1):
        for j in expired._rows:
            if j[1] == finallist[i - 1]:
                mylist = j
                mylist.insert(0, f"{i}.")
                expiredfinal.add_row(mylist)
    del expired
    expired = expiredfinal
    count = 0
    while True:
        if len(expired.get_string()) <= 2000:
            active_con = discord.Embed(description=f"```css\n{expired}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            explist.append(active_con)
            break
        else:
            if count > len(expired.get_string()): break
            active_con = discord.Embed(description=f"```css\n{expired.get_string()[count:2000]}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            count += 2000
            explist.append(active_con)

    return {"active":actlist, "expired":explist}

async def handle_1(userid):
    warn1.append(userid)
    await asyncio.sleep(2)
    warn1.remove(userid)

async def handle_2(userid):
    warn2.append(userid)
    await asyncio.sleep(2)
    warn2.remove(userid)

async def handle_disregard(userid):
    disregarded.append(userid)
    await asyncio.sleep(10*60)
    disregarded.remove(userid)

async def general(ctx):
    state = await spam_protect(ctx.author.id)
    toreturn = True
    if state == 'warn':
        embed = discord.Embed(description=f'{economyerror} You are being rate-limited for using commands too fast!\nTry again in few secs..', color=error_embed)
        await ctx.send(embed=embed)
        toreturn = False
    elif state == 'disregard':
        embed = discord.Embed(title=f'{economyerror} Warning!',
                              description=f'{ctx.author.mention} has been disregarded for 10 mins!\n**Reason: Spamming Commands**',
                              color=error_embed)
        await ctx.send(embed=embed)
        toreturn= False
    elif state == 'return':
        toreturn= False
    return toreturn

async def close_admin(a):
    bot.refr["719946380285837322"] = a
    chl = bot.get_channel(854692793276170280)
    await chl.send(json.dumps(bot.refr))

async def updateuserdata():
    chl = bot.get_channel(856070919033978932)
    with open("userdata.json", "w") as f:
        f.write(json.dumps(bot.userdata, indent=2))
    await chl.send(file=discord.File("userdata.json"))

async def auto_update():
    while True:
        await update_embeds("VNTA")
        files = bot.get_channel(854698116255318057)
        with open("botdata.json", "w") as f:
            f.write(str(json.dumps(bot.data, indent=2)))
        #await files.send(file=discord.File("botdata.json"))
        await asyncio.sleep(300)

async def update_embeds(clan):
    await bot.wait_until_ready()
    all_data = bot.refr[clan]
    channel = bot.get_channel(all_data["chl"])

    actlist = []
    explist = []
    for msgs in all_data["active"]:
        active = await channel.fetch_message(msgs)
        actlist.append(active)

    for msgs in all_data["expired"]:
        expired = await channel.fetch_message(msgs)
        explist.append(expired)
    
    data = await embed_view(clan)
    if len(data["active"]) == len(actlist):
        count = 0
        for i in data["active"]:
            i.set_footer(text=f"Bot by {bot.dev} | Last Refreshed", icon_url=sampfp)
            i.timestamp = datetime.datetime.utcnow()
            await actlist[count].edit(embed=i)
    else:
        return await view(channel, via="sam123", clan=clan)

    if len(data["expired"]) == len(actlist):
        for i in data["expired"]:
            count = 0
            i.set_footer(text=f"Bot by {bot.dev} | Last Refreshed", icon_url=sampfp)
            i.timestamp = datetime.datetime.utcnow()
            await explist[count].edit(embed=i)
    else:
        return await view(channel, via="sam123", clan=clan)

async def update_links():
    with open("links.json", "w") as f:
        f.write(str(json.dumps(bot.links, indent=2)))
    await bot.get_channel(854721559359913994).send(file=discord.File("links.json"))

async def get_admin():
    return bot.refr["719946380285837322"]

async def spam_protect(userid):
    if userid in disregarded:
        if userid not in devs: return 'return'
        else: return 'ok'
    last = usercmds.get(userid, 0)
    current = time.time()
    usercmds[userid] = current
    if current - last < 2:
        if userid in warn2:
            asyncio.create_task(handle_disregard(userid))
            return 'disregard'
        elif userid in warn1:
            asyncio.create_task(handle_2(userid))
            return 'warn'
        else:
            asyncio.create_task(handle_1(userid))
            return 'warn'
    else:
        return 'ok'

async def sendnew(ctx, vntadat, ign):
    curset = f"1. Headings Color- {vntadat['hd']}\n" \
             f"2. Stats Color- {vntadat['st']}\n" \
             f"3. Motto Text- {vntadat['mt']}\n" \
             f"4. Username Color- {vntadat['us']}\n" \
             f"5. Bottom Text Color- {vntadat.get('bt', [0,0,0])}"
    embed = discord.Embed(title="⚙️ VNTA Profile Background",
                          description="Current Settings:\n" \
                                      f"```less\n{curset}```\n"
                                      "__Choose the below options to modify the background:__\n\n" \
                                      "`modify 1` - Change background image\n" \
                                      "`modify 2` - Change headings color\n" \
                                      "`modify 3` - Change stats color\n" \
                                      "`modify 4` - Change background motto\n" \
                                      "`modify 5` - Change username color\n"
                                      "`modify 6` - Change bottom text color",
                          color=embedcolor)
    embed.set_image(url=f"attachment://profile.{vntadat['file'].lower()[-3:]}")
    file = await profile(ctx, ign={"main":ign}, via=True)
    embed.set_footer(text="Type 'save' to save background\nType 'cancel' to cancel all changes")
    await ctx.send(embed=embed, file=file)

async def savebgdata():
    with open("bgdata.json", "w") as f:
        f.write(json.dumps(bot.bgdata, indent=2))
    chl = bot.get_channel(854698116255318057)
    await chl.send(file=discord.File("bgdata.json"))

staffchl = [813447381752348723, 854008993248051230]
@bot.command()
@commands.check(general)
async def view(channel, clan=None, via=None):
    if bot.pause: return await channel.send("⚠ ️Maintainence Update. Please retry later")
    if bot.cwpause:
        embed = discord.Embed(title="Wars Break",
                              description="Clan wars are not currently running. Please use this command after wars start!",
                              colour=error_embed)
        return await channel.reply(embed=embed)
    if via == "sam123" and clan is not None:
        pass
    else:
        if not any(allow in [role.id for role in channel.author.roles] for allow in accepted):
            return await channel.reply("Only VNTA members are given the exclusive rights to use the bot.")
        if clan is not None:
            if not any(allow in [role.id for role in channel.author.roles] for allow in staff):
                print("not qual")
                clan = "VNTA"
            else:
                if channel.channel.id not in staffchl:
                    return await channel.reply(f"For security reasons, this command cannot be used in a public channel.\n"
                                           f"Please go to {' or '.join([x.mention for x in [bot.get_channel(y) for y in staffchl]])}.")
        else:
            clan = "VNTA"
        if channel.channel.id not in [813437673926557736, 813447381752348723, 854008993248051230]:
            return await channel.reply(
                "Please go to <#813437673926557736> or <#813447381752348723> to use `v.view` or `v.end`")
        channel = channel.channel
    data = await embed_view(clan)
    maybeupdate = {}
    for i in data.keys():
        em = data[i]
        ids = []
        for j in em:
            a = await channel.send(embed=j)
            ids.append(a.id)

        if via == "sam123" and clan is not None:
            maybeupdate[i] = ids
    if len(maybeupdate.values()) != 0:
        maybeupdate["chl"] = channel.id
        bot.refr[clan] = maybeupdate
        await update_embeds(clan)

@bot.command()
@commands.is_owner()
async def sizes(ctx):
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Yi', suffix)

    allsizes = ""
    for name, size in sorted(((name, sys.getsizeof(value)) for name, value in globals().items()),
                             key=lambda x: -x[1])[:10]:
        allsizes += "{:>30}: {:>8}".format(name, sizeof_fmt(size))
    with open("sizes.txt", "w") as f:
        f.write(allsizes)
    await ctx.reply(file=discord.File("sizes.txt"))

@bot.command()
@commands.check(general)
@commands.has_permissions(manage_channels=True)
async def refresh(ctx, what:str=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    clan = "VNTA"
    if what is None:
        await update_embeds(clan)
        await ctx.message.add_reaction("✅")
    elif what == "setup":
        await view(ctx.channel, via="sam123", clan=clan)
        chl = bot.get_channel(854692793276170280)
        await chl.send(str(json.dumps(bot.refr)))

staff = [813441664617939004, 855793126958170122, 853997809212588073]
@bot.command()
@commands.check(general)
async def end(ctx, clan=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if bot.cwpause:
        embed = discord.Embed(title="Wars Break",
                              description="Clan wars are not currently running. Please use this command after wars start!",
                              colour=error_embed)
        return await ctx.reply(embed=embed)
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    if clan is not None:
        if not any(allow in [role.id for role in ctx.author.roles] for allow in staff):
            clan = "VNTA"
        else:
            if ctx.channel.id not in staffchl:
                return await ctx.reply(f"For security reasons, this command cannot be used in a public channel.\n"
                                       f"Please go to {' or '.join([x.mention for x in [bot.get_channel(y) for y in staffchl]])}.")
    else:
        clan = "VNTA"
    if ctx.channel.id not in [813437673926557736, 813447381752348723, 854008993248051230]:
        return await ctx.reply("Please go to <#813437673926557736> or <#813447381752348723> to use `v.view` or `v.end`")
    data = await getdata(clan)
    data = data["data"]["members"]
    active = PrettyTable()
    active.field_names = ["Player Name", "Kills", "Estd. Kills", "Time Played"]

    activefinal = PrettyTable()
    activefinal.field_names = ["S.No.", "Player Name", "Kills", "Est. Kills", "Time Played"]
    sno = 1
    finalkills = 0
    act = 1
    exp = 1
    for i in data:
        j = i
        i = i["contract"]
        timeplayed = int(i["timeplayed"] / 1000)
        left = datetime.timedelta(seconds=timeplayed)
        final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
        colon_format = str(final).split(" ")[1].split(':')

        if timeplayed == 0:
            est = 0
        elif timeplayed > 10800:
            est = i["kills"]
        else:
            est = int((i["kills"]/timeplayed)*10800)
        finalkills += est
        if timeplayed < 10800 and timeplayed != 0:
            active.add_row([j["username"], i["kills"], est,
                            f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            act += 1

    active.sortby = "Estd. Kills"
    active.reversesort = True
    activefinal.title = f"Estimated Kills- {finalkills}"
    finallist = []
    for i in active._rows:
        finallist.append(i[2])
    finallist.sort(reverse=True)
    for i in range(1, len(finallist) + 1):
        for j in active._rows:
            if j[2] == finallist[i - 1]:
                mylist = j
                active._rows.remove(j)
                mylist.insert(0, f"{i}.")
                activefinal.add_row(mylist)
    del active
    active = activefinal
    actlist = []
    explist = []

    count = 0
    while True:
        if len(active.get_string()) <= 2000:
            active_con = discord.Embed(description=f"```css\n{active}```",
                                       color=color)
            actlist.append(active_con)
            break
        else:
            if count > len(active.get_string()): break
            active_con = discord.Embed(description=f"```css\n{active.get_string()[count:2000]}```",
                                       color=color)
            count += 2000
            actlist.append(active_con)

    for j in actlist:
        j.set_footer(text=f"Est. Kills: {finalkills} | Bot by {bot.dev}", icon_url=sampfp)
        a = await ctx.send(embed=j)

@bot.command(aliases=['eval'],hidden=True)
@commands.is_owner()
async def evaluate(ctx, *, expression):
    try:
        await ctx.reply(eval(expression))
        await ctx.message.add_reaction(economysuccess)
    except Exception as e:
        await ctx.reply(f'```\n{e}```')

@bot.command(aliases=['exec'],hidden=True)
@commands.is_owner()
async def execute(ctx, *, expression):
    try:
        exec(expression)
        await ctx.message.add_reaction(economysuccess)
    except Exception as e:
        await ctx.reply(f'Command:```py\n{expression}```\nOutput:```\n{e}```')

accepted = [813786315530305536, 813527378088951809, 813527377736761384, 813452412810690600, 813441662588157952, 836427405656326165, 853997809212588073]
@bot.command()
@commands.is_owner()
async def test(ctx):
    copy_d = copy.copy(bot.links)
    new = {}
    for i in copy_d.keys():
        new[i] = copy_d[i]["main"]
    bot.links.clear()
    bot.links = new
    await update_links()

bot.pendings = {}
@bot.command()
@commands.check(general)
async def link(ctx, *, ign):
    staff = bot.get_channel(855450311808122951)
    a = await staff.send(f"{ctx.author.mention} wants to link with {ign}")
    await a.add_reaction("✅")
    await a.add_reaction("❌")
    bot.pendings[a.id] = (ctx.author.id, str(ign))
    embed = discord.Embed(description=f"Link request submitted to staff successfully!", color=success_embed)
    await ctx.reply(embed=embed)

@bot.command(aliases=["con"])
@commands.check(general)
async def contract(ctx, *, ign=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if bot.cwpause:
        embed = discord.Embed(title="Wars Break",
                              description="Clan wars are not currently running. Please use this command after wars start!",
                              colour=error_embed)
        return await ctx.reply(embed=embed)
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    if ign is None:
        ign = bot.links.get(str(ctx.author.id))
        if ign is None:
            embed = discord.Embed(description="You aren't linked yet. Use `v.link <ign>` to get linked.\n"
                                              "Or use `v.contract <ign>` to view",
                                  color=16730441)
            embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing")
            return await ctx.reply(embed=embed)
        ign = ign["main"]
    else:
        newign = str(ign).replace('<@!', '').replace('>', '')
        if len(newign) == len("537623052775718912"):
            ign = bot.links.get(str(newign))
            work = bot.userdata.get(str(newign), {"incognito": False})["incognito"]
            if work and ctx.author.id != int(newign): ign = None
            if ign is None:
                embed = discord.Embed(description="User not linked yet.",
                                      color=error_embed)
                embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing")
                return await ctx.reply(embed=embed)
            ign = ign["main"]

    data = await getdata("VNTA")
    data = data["data"]["members"]
    found = False
    for i in data:
        if ign.lower() == i["username"].lower():
            userdata = i
            con = i["contract"]
            found = True
            break
    if not found:
        return await ctx.reply("User not in VNTA or incorrect IGN!")
    timeplayed = int(con["timeplayed"] / 1000)
    left = datetime.timedelta(seconds=timeplayed)
    if timeplayed > 10800:
        tleft = 0
    else:
        tleft = 10800 - timeplayed
    diff = (timeplayed/10800)
    hours, remainder = divmod(int(timeplayed), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    hours2, remainder2 = divmod(int(tleft), 3600)
    minutes2, seconds2 = divmod(remainder2, 60)
    days2, hours2 = divmod(hours2, 24)

    games = timeplayed / 240
    if timeplayed == 0:
        est = 0
        kpg = 0
    else:
        est = int((con["kills"] / timeplayed) * 10800)
        kpg = con["kills"]/games
    img = Image.open("bgs/contract.png")
    font = ImageFont.truetype("bgs/font.ttf", 14)
    font2 = ImageFont.truetype("bgs/font.ttf", 18)
    shadow = Image.new("RGBA", img.size)
    draw2 = ImageDraw.Draw(shadow)
    order = [str(con["kills"]), str(con["deaths"]), "{:.2f}".format(kpg), "{:.2f}".format(kpg/4)]

    xloc = 60
    for i in order:
        draw2.text((xloc - (font.getsize(i)[0] / 2), 110), i, font=font, fill=(0,0,0))
        xloc += 111
    draw2.text((330, 155), f"{hours}h {minutes}m {seconds}s", font=font, fill=(0,0,0))
    draw2.text((160, 187), str(est), font=font, fill=(0,0,0))
    draw2.text((225 - (font2.getsize(userdata['username'])[0]) / 2, 40), str(userdata["username"]), font=font2, fill=(0,0,0))
    draw2.text((160, 216), f"{hours2}h {minutes2}m {seconds2}s", font=font, fill=(0,0,0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=2))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    xloc = 60
    for i in order:
        draw.text((xloc-(font.getsize(i)[0]/2), 110), i, font=font)
        xloc += 111
    draw.text((330, 155), f"{hours}h {minutes}m {seconds}s", font=font)
    draw.text((160, 187), str(est), font=font)
    draw.text((225-(font2.getsize(userdata['username'])[0])/2, 40), str(userdata["username"]), font=font2, fill=(255, 251, 57))
    draw.text((160, 216), f"{hours2}h {minutes2}m {seconds2}s", font=font)

    xpbar = Image.open("bgs/xpbar.png")
    pixdata = xpbar.load()
    for y in range(xpbar.size[1]):
        for x in range(xpbar.size[0]):
            pixdata[x, y] = tuple(list((255, 123, 57)) + [pixdata[x, y][-1]])
    xpbar = xpbar.crop((0, 0, xpbar.width*diff, xpbar.height))
    img.paste(xpbar, (10, 157), xpbar)

    imagebytes = BytesIO()
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2)
    img.save(imagebytes, "PNG")
    imagebytes.seek(0)
    embed = discord.Embed(color=4521960)
    embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing", icon_url=sampfp)
    embed.set_image(url="attachment://contract.png")
    await ctx.send(embed=embed, file=discord.File(imagebytes, filename="contract.png"))

@bot.command(aliases=["p", "pf"])
@commands.check(general)
async def profile(ctx, *, ign=None, via=False):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if ign is None:
        ign = bot.links.get(str(ctx.author.id))
        if ign is None:
            embed = discord.Embed(description="You aren't linked yet. Use `v.link <ign>` to get linked.\n"
                                              "Or use `v.pf <ign>` to view",
                                  color=16730441)
            embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing")
            return await ctx.reply(embed=embed)
        ign = ign["main"]
    else:
        newign = str(ign).replace('<@!', '').replace('>', '')
        if len(newign) == len("537623052775718912"):
            ign = bot.links.get(str(newign))
            work = bot.userdata.get(str(ctx.author.id), {"incognito": False})["incognito"]
            if work and ctx.author.id != int(newign): ign = None
            if ign is None:
                embed = discord.Embed(description="User not linked yet.",
                                      color=error_embed)
                embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing")
                return await ctx.reply(embed=embed)
            ign = ign["main"]
    if type(ign) == dict:
        ign = ign["main"]
    bgdata = {}
    found = False
    for i in bot.bgdata.keys():
        if i.lower() == ign.lower():
            bgdata = bot.bgdata[i]
            found = True
            break
    if via:
        for i in bot.unsaved.keys():
            if i.lower() == ign.lower():
                newbgdata = bot.unsaved[i]
                if newbgdata["file"] != "":
                    bgdata = newbgdata
                    found = True
                    break
    if not found:
        bgdata = bot.bgdata["vntasam123"]
    print(bgdata)
    data = requests.get(f"https://kr.vercel.app/api/profile?username={ign}")
    if data.status_code != 200:
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        return await ctx.send(embed=embed)
    userdata = json.loads(data.text)
    #userdata = {'success': True, 'data': {'username': 'AwesomeSam', 'id': 8570737, 'clan': 'VNTA', 'clanRank': 6, 'kills': 82112, 'deaths': 41107, 'wins': 2871, 'score': 9299165, 'level': 91, 'levelPercentage': {'percent': 48.22, 'current': 98053.89, 'max': 203333.33}, 'games': 5830, 'funds': 3533, 'hacker': False, 'verified': False, 'infected': True, 'partner': 1, 'premium': -17955973000, 'premiumName': 'AwesomeSam', 'timePlayed': 1243629476, 'createdAt': '2019-12-19T07:56:22.000Z', 'stats': {'c': 5, 's': 1348599, 'h': 311836, 'c0': 3845230, 'r2': 3815, 'c1': 1753660, 'c2': 1944840, 'mk': 957, 'c5': 563205, 'c4': 91655, 'c8': 145775, 'c7': 66375, 'r3': 20, 'c12': 107410, 'hs': 49704, 'wb': 586, 'flg': 94, 'c9': 75640, 'c11': 336455, 'c6': 37865, 'c3': 131965, 'abR': 1605354754870, 'n': 34, 'chgP': '19:0,0,30,1000', 'anp': 0, 'c13': 274540, 'r4': 18, 'tk': 71, 'fk': 105, 'tmk': 1081, 'r1': 8, 'ast': 1203, 'ls': 741, 'ad': 57, 'spry': 9, 'sad': 1, 'cad': 1}, 'challenge': 19, 'twitch': 'awesomesamaksh', 'elo': 49.58, 'elo2': 0, 'elo4': None, 'followers': 303, 'following': 70, 'region': 2, 'eventCount': None, 'mods': [], 'maps': [{'name': 'Hell_Parkour', 'id': 119179, 'info': {'t': 1}, 'votes': 30, 'verified': None, 'createdAt': '2021-02-03T07:18:50.000Z', 'creator': 'AwesomeSam'}], 'assets': [], 'skins': []}, 'time': 0.169}
    if not userdata["success"]:
        return await ctx.reply(userdata["error"])
    userdata = userdata["data"]
    username = userdata["username"]
    clan = userdata["clan"]
    kills = userdata["kills"]
    deaths = userdata["deaths"]
    kr = userdata["funds"]
    datestr = userdata["createdAt"].split("T")[0]
    wins = userdata["wins"]
    score = userdata["score"]
    level = userdata["level"]
    played = userdata["games"]
    loses = played - wins
    challenge = userdata["challenge"]
    if challenge is None: challenge = 0
    else: challenge = int(challenge) + 1
    nukes = userdata["stats"].get("n", 0)
    headshots = userdata["stats"].get("hs", 0)
    shots = userdata["stats"].get("s", 0)
    hits = userdata["stats"].get("h", 0)
    timeplayed = int(userdata["timePlayed"]/1000)
    melee = userdata["stats"].get("mk", 0)
    wallbangs = userdata["stats"].get("wb", 0)
    date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d')
    now = datetime.datetime.now()
    daysplayed = (now-date_obj).days
    mpk = "{:.2f}".format((shots - hits)/kills)
    hps = "{:.2f}%".format((headshots/hits)*100)
    gpn = "{:.2f}".format(played/nukes)
    npd = "{:.2f}".format(nukes/ daysplayed)
    kpg = "{:.2f}".format(kills/played)
    kpm = "{:.2f}".format(float(kpg)/4)
    if loses == 0: loses = 1
    wl = "{:.2f}".format(wins/loses)
    kdr = "{:.4f}".format(kills/deaths)
    spk = "{:.2f}".format(score/kills)
    avgscore = int(score/played)
    accuracy = "{:.2f}%".format((hits/shots)*100)
    statsoverlay = Image.new("RGBA", (1280, 720))
    borders = Image.open("bgs/borders.png")

    if bgdata["ov"]:
        overlay = Image.open("bgs/overlay.png")
        borders.paste(overlay, (0, 0), overlay)

    statsoverlay.paste(borders, (0, 0))

    # ============ DRAWING STARTS ==============
    order = [["Score", "Kills", "Deaths", "KR", "Playtime", "Nukes"],
             ["Played", "Won", "Lost", "W/L", "KDR", "Challenge"],
             ["MPK", "SPK", "GPN", "NPD", "KPM", "KPG"],
             ["Avg. Score", "Accuracy", "Headshots", "HPS", "Melee", "Wallbangs"]]
    draw = ImageDraw.Draw(statsoverlay)
    shadow = Image.new("RGBA", statsoverlay.size)
    draw2 = ImageDraw.Draw(shadow)
    font = ImageFont.truetype("bgs/font.ttf", 20)
    font2 = ImageFont.truetype("bgs/font.ttf", 40)
    font3 = ImageFont.truetype("bgs/font.ttf", 26)
    font4 = ImageFont.truetype("bgs/font.ttf", 22)

    yloc = 148
    for row in order:
        xloc = 105
        for stat in row:
            size = font4.getsize(str(stat))[0]
            draw2.text((xloc - (size / 2), yloc), str(stat), font=font4, fill=(0, 0, 0))
            xloc += 214
        yloc += 119

    yloc = 148
    for row in order:
        xloc = 105
        for stat in row:
            size = font4.getsize(str(stat))[0]
            draw.text((xloc - (size / 2), yloc), str(stat), font=font4, fill=tuple(bgdata["hd"]))
            xloc += 214
        yloc += 119
    if bgdata["file"] == "":
        bgdata["file"] = bot.bgdata["vntasam123"]["file"]
    try:
        r = requests.get(bgdata["file"], stream=True)
        imgtype = bgdata['file'].lower()[-3:]
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(f"bgs/{ctx.author.id}.{imgtype}", 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else: raise ValueError
        bgimage = Image.open(f"bgs/{ctx.author.id}.{imgtype}")
    except:
        bot.bgdata[ign]["file"] = ""
        await savebgdata()
        return await ctx.send(f"Background Corrupted. It is auto-removed. Please set again using `v.pbg`")
    if imgtype == "png":
        bgimage = bgimage.convert("RGBA").resize((1280, 720))
    order = [[score, kills, deaths, kr, timeplayed, nukes],
              [played, wins, loses, wl, kdr, challenge],
              [mpk, spk, gpn, npd, kpm, kpg],
              [avgscore, accuracy, headshots, hps, melee, wallbangs]]

    if challenge > 20:
        fill = (255, 43, 43)
    elif challenge > 15:
        fill = (228, 70, 255)
    elif challenge > 10:
        fill = (255, 130, 58)
    else:
        fill = (36, 36, 36)
    user = "???"
    for key, value in bot.links.items():
        if value["main"].lower() == username.lower():
            work = bot.userdata.get(str(key), {"incognito": False})["incognito"]
            if not work:
                user = await bot.fetch_user(int(key))
                user = f"{user.name}#{user.discriminator}"
            break

    yloc = 191
    for row in order:
        xloc = 104
        for stat in row:
            size = font.getsize(str(stat))[0]
            draw2.text((xloc-(size/2), yloc), str(stat), font=font, fill=(0,0,0))
            xloc += 214
        yloc += 119
    #draw2.text((35, 32), str(level), fill=(0,0,0), font=font2)

    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=2))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))
    frm = []
    if imgtype == "png":
        bgimage = Image.alpha_composite(bgimage, shadow)
    else:
        for fr in ImageSequence.Iterator(bgimage):
            fr = fr.convert("RGBA")
            fr = fr.resize((1280, 720))
            frm.append(Image.alpha_composite(fr, shadow))

    yloc = 191
    for row in order:
        xloc = 104
        for stat in row:
            size = font.getsize(str(stat))[0]
            draw.text((xloc - (size / 2), yloc), str(stat), font=font, fill=tuple(bgdata["st"]))
            xloc += 214
        yloc += 119
    rank = userdata["clanRank"]
    if rank == 1:
        clancolor = (162, 255, 74)
    elif rank <= 3:
        clancolor = (50, 50, 50)
    elif rank <= 10:
        clancolor = (255, 50, 50)
    elif rank <= 20:
        clancolor = (255, 255, 70)
    elif rank <= 30:
        clancolor = (224, 64, 255)
    elif rank <= 50:
        clancolor = (46, 155, 254)
    else:
        clancolor = (180, 180, 180)
    if clan == "VIP":
        clancolor = (68, 255, 25)
    elif clan == "DEV":
        clancolor = (25, 191, 255)
    draw.text((1173-font3.getsize(bgdata['mt'])[0], 655), bgdata["mt"], fill=tuple(bgdata.get("bt", [0,0,0])), font=font3)
    draw.text((35, 32), str(level), fill=fill, font=font2)
    draw.text((65+font2.getsize(str(level))[0], 32), str(username), fill=tuple(bgdata["us"]), font=font2)
    draw.text((85+font2.getsize(str(level))[0]+font2.getsize(str(username))[0], 32), f"[{clan}]", fill=clancolor, font=font2)
    draw.text((120, 655), user, font=font3, fill=tuple(bgdata.get("bt", [0,0,0])))
    dis_logo = Image.open("bgs/discord.png").resize((69, 69))
    statsoverlay.paste(dis_logo, (30, 639))

    image_bytes = BytesIO()
    if imgtype == "png":
        bgimage = Image.alpha_composite(bgimage, statsoverlay)
        bgimage.save(image_bytes, 'PNG')
        image_bytes.seek(0)
    else:
        final = []
        for i in frm:
            final.append(Image.alpha_composite(i, statsoverlay))
        final[0].save(image_bytes,
                    format='GIF',
                    save_all=True,
                    append_images=final[1:],
                    loop=0)
        image_bytes.seek(0)
    statsoverlay.close()
    bgimage.close()
    if not via:
        await ctx.send(file=discord.File(image_bytes, filename=f"profile.{imgtype}"))
    else:
        return discord.File(image_bytes, filename=f"profile.{imgtype}")

@bot.command(aliases=["incog"])
@commands.check(general)
async def incognito(ctx):
    data = bot.userdata.setdefault(str(ctx.author.id), {"incognito":False})
    if data["incognito"]:
        data["incognito"] = False
        embed=discord.Embed(description=f"{economysuccess} You are **no longer** in incognito mode", color=success_embed)
        await ctx.reply(embed=embed)
    else:
        data["incognito"] = True
        embed = discord.Embed(description=f"{economysuccess} You are in incognito mode", color=success_embed)
        await ctx.reply(embed=embed)
    bot.userdata[str(ctx.author.id)] = data
    await updateuserdata()

@bot.command()
@commands.check(general)
async def cbg(ctx):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if not any(allow in [role.id for role in ctx.author.roles] for allow in staff):
        return
    if "vntasam123" in bot.already:
        return await ctx.reply("Someone is already editing this background. Please wait")
    bot.already.append("vntasam123")
    bot.unsaved["vntasam123"] = copy.copy(bot.bgdata["vntasam123"])
    await sendnew(ctx, bot.unsaved["vntasam123"], "AwesomeSam")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        while True:
            print(bot.bgdata, bot.unsaved)
            mainmsg = await bot.wait_for("message", check=check, timeout=180)
            msgc = mainmsg.content.lower()
            if msgc == "cancel":
                bot.already.remove("vntasam123")
                break
            elif msgc == "save":
                bot.bgdata["vntasam123"] = bot.unsaved["vntasam123"]
                await savebgdata()
                bot.already.remove("vntasam123")
                await ctx.send(f"{economysuccess} Saved Successfully!")
            elif msgc == "modify 1":
                try:
                    embed = discord.Embed(description="Upload the `PNG/GIF` file from your PC to set as background.\n"
                                                      "**Dont send a link to the image! Attach the file**",
                                          color=embedcolor)
                    embed.set_footer(text="Recommended Size: 1280x720")
                    await ctx.send(embed=embed)

                    msg = await bot.wait_for("message", check=check, timeout=180)
                    try:
                        image = msg.attachments[0].url
                        if image[-3:].lower() not in ["png", "gif"]:
                            await ctx.send(f"{ctx.author.mention} The image should be `.PNG/.GIF` file only!")
                            continue
                        r = requests.get(image, stream=True)
                        if r.status_code == 200:
                            r.raw.decode_content = True
                            with open(f"bgs/{ctx.author.id}.png", 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                            bgfile = await bot.get_channel(856723935357173780).send(
                                file=discord.File(f"bgs/{ctx.author.id}.{image[-3:].lower()}", filename=f"{ctx.author.id}.{image[-3:].lower()}"))
                            bot.unsaved["vntasam123"]["file"] = bgfile.attachments[0].url
                            await ctx.send(f"Done!")
                            await sendnew(ctx, bot.unsaved["vntasam123"], "AwesomeSam")
                        else:
                            await ctx.send(f"Error fetching image, Please contact {bot.dev} for help.")
                    except:
                        await ctx.send("Bot didnt detect any attachments. Make sure you upload the image from your device!")
                except asyncio.TimeoutError:
                    pass
            elif msgc in ["modify 2", "modify 3", "modify 5", "modify 6"]:
                try:
                    embed = discord.Embed(description="Enter the `R, G, B` code or `#Hex` value of the color.\n"
                                                      "Trouble choosing? [Click Here](https://htmlcolorcodes.com/)\n",
                                          color=embedcolor)
                    await ctx.send(embed=embed)
                    try:
                        msg = await bot.wait_for("message", check=check, timeout=180)
                        if msg.content[0] == "#":
                            h = msg.content.lower().lstrip('#')
                            r, g, b = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
                        else:
                            r, g, b = msg.content.replace(" ", "").split(",")
                        r = int(r)
                        g = int(g)
                        b = int(b)
                        if (r>255 or r<0) or (g>255 or g<0) or (b>255 or b<0): raise ValueError

                        types = {2: "hd", 3: "st", 5: "us", 6:"bt"}
                        print(bot.bgdata)
                        print(bot.unsaved)
                        bot.unsaved["vntasam123"][types[int(msgc[-1])]] = [r, g, b]
                        await ctx.send("Done!")
                        print()
                        print(bot.bgdata)
                        print(bot.unsaved)
                        await sendnew(ctx, bot.unsaved["vntasam123"], "AwesomeSam")
                    except:
                        await ctx.send("Incorrect `R, G, B` / `#Hex` code. Please retry")
                except asyncio.TimeoutError:
                    pass
            elif msgc == "modify 4":
                try:
                    embed = discord.Embed(description="Enter the motto for your background. Make sure it is not NSFW type",
                                          color=embedcolor)
                    embed.set_footer(text="Type 'default' to remove")
                    await ctx.send(embed=embed)
                    try:
                        msg = await bot.wait_for("message", check=check, timeout=180)
                        if msg.content.lower() != "default":
                            bot.unsaved["vntasam123"]["mt"] = msg.content
                        else:
                            bot.unsaved["vntasam123"]["mt"] = ""
                        await ctx.send("Done!")
                        await sendnew(ctx, bot.unsaved["vntasam123"], "AwesomeSam")
                    except:
                        await ctx.send(f"Unknown error occured. Pleasr contact {bot.dev}")
                except asyncio.TimeoutError:
                    pass
    except asyncio.TimeoutError:
        pass

@bot.command()
@commands.check(general)
async def main(ctx, *, ign):
    d = bot.links.get(str(ctx.author.id))
    if d is None:
        return await ctx.send("You have no accounts linked. Use `v.link <ign>` to link an account first")
    if ign.lower() not in [x.lower() for x in d["all"]]:
        return await ctx.send("This account isnt linked to you")
    d["main"] = ign.lower()
    bot.links[str(ctx.author.id)] = d
    await update_links()
    embed=discord.Embed(description=f"{economysuccess} Done! `{ign}` is now your main account", color=success_embed)
    await ctx.reply(embed=embed)

@bot.command()
@commands.check(general)
async def pbg(ctx, *, ign=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if ign is not None and ctx.author.id in devs:
        print("Dev edit-", ign)
        ign = {"main":ign}
    else:
        ign = bot.links.get(str(ctx.author.id))
    if ign is None:
        return await ctx.reply("You need to be linked to get a custom background")
    ign = ign["main"]
    if (ign.lower() not in bot.vntapeeps):
        if ign.lower() not in bot.excl:
            return await ctx.send("Only VNTA clan members or people with exculsive permission from developer can use this command")

    if ign in bot.already:
        return await ctx.reply("Someone is already editing this background. Please wait")
    bot.already.append(ign)
    defign = {"file":"",
              "hd":[0,0,0],
              "st":[222, 222, 222],
              "mt":"",
              "us":[30, 30, 36],
              "ov":True}
    bot.unsaved[ign] = copy.copy(bot.bgdata.get(ign, defign))
    await sendnew(ctx, bot.unsaved[ign], ign)
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        while True:
            mainmsg = await bot.wait_for("message", check=check, timeout=180)
            msgc = mainmsg.content.lower()
            if msgc == "cancel":
                await mainmsg.add_reaction(economysuccess)
                bot.already.remove(ign)
                break
            elif msgc == "save":
                bot.bgdata[ign] = bot.unsaved[ign]
                await savebgdata()
                bot.already.remove(ign)
                await ctx.send(f"{economysuccess} Saved Successfully!")
            elif msgc == "modify 1":
                try:
                    embed = discord.Embed(description="Upload the `PNG/GIF` file from your PC to set as background.\n"
                                                      "**Dont send a link to the image! Attach the file**",
                                          color=embedcolor)
                    embed.set_footer(text="Recommended Size: 1280x720")
                    await ctx.send(embed=embed)

                    msg = await bot.wait_for("message", check=check, timeout=180)
                    try:
                        image = msg.attachments[0].url
                        if image[-3:].lower() not in ["png", "gif"]:
                            await ctx.send(f"{ctx.author.mention} The image should be `.PNG/.GIF` file only!")
                            continue
                        r = requests.get(image, stream=True)
                        if r.status_code == 200:
                            r.raw.decode_content = True
                            with open(f"bgs/{ctx.author.id}.{image[-3:].lower()}", 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                            bgfile = await bot.get_channel(856723935357173780).send(file=discord.File(f"bgs/{ctx.author.id}.{image[-3:].lower()}", filename=f"{ctx.author.id}.{image[-3:].lower()}"))
                            bot.unsaved[ign]["file"] = bgfile.attachments[0].url
                            await ctx.send(f"Done!")
                            await sendnew(ctx, bot.unsaved[ign], ign)
                        else:
                            await ctx.send(f"Error fetching image, Please contact {bot.dev} for help.")
                    except Exception as e:
                        print(e)
                        await ctx.send("Bot didnt detect any attachments. Make sure you upload the image from your device!")
                except asyncio.TimeoutError:
                    pass
            elif msgc in ["modify 2", "modify 3", "modify 5", "modify 6"]:
                try:
                    embed = discord.Embed(description="Enter the `R, G, B` code or `#Hex` value of the color.\n"
                                                      "Trouble choosing? [Click Here](https://htmlcolorcodes.com/)\n",
                                          color=embedcolor)
                    await ctx.send(embed=embed)
                    try:
                        msg = await bot.wait_for("message", check=check, timeout=180)
                        if msg.content[0] == "#":
                            h = msg.content.lower().lstrip('#')
                            r, g, b = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
                        else:
                            r, g, b = msg.content.replace(" ", "").split(",")
                        r = int(r)
                        g = int(g)
                        b = int(b)
                        if (r>255 or r<0) or (g>255 or g<0) or (b>255 or b<0): raise ValueError

                        types = {2: "hd", 3: "st", 5: "us", 6:"bt"}
                        bot.unsaved[ign][types[int(msgc[-1])]] = [r, g, b]
                        await ctx.send("Done!")
                        await sendnew(ctx, bot.unsaved[ign], ign)
                    except:
                        await ctx.send("Incorrect `R, G, B` / `#Hex` code. Please retry")
                except asyncio.TimeoutError:
                    pass
            elif msgc == "modify 4":
                try:
                    embed = discord.Embed(description="Enter the motto for your background. Make sure it is not NSFW type",
                                          color=embedcolor)
                    embed.set_footer(text="Type 'default' to remove")
                    await ctx.send(embed=embed)
                    try:
                        msg = await bot.wait_for("message", check=check, timeout=180)
                        if msg.content.lower() != "default":
                            bot.unsaved[ign]["mt"] = msg.content
                        else:
                            bot.unsaved[ign]["mt"] = ""
                        await ctx.send("Done!")
                        await sendnew(ctx, bot.unsaved[ign], ign)
                    except:
                        await ctx.send(f"Unknown error occured. Pleasr contact {bot.dev}")
                except asyncio.TimeoutError:
                    pass
    except asyncio.TimeoutError:
        bot.already.remove(ign)

@bot.command()
@commands.check(general)
async def alts(ctx, mem:discord.Member=None):
    if id is None:
        d = bot.links.get(str(ctx.author.id))
    else:
        d = bot.links.get(str(mem.id))
    if d is None:
        return await ctx.send("You have no accounts linked. Use `v.link <ign>` to link an account first")
    altslist = "\n".join(d["all"])
    s = f"```css\n{altslist}```"
    embed= discord.Embed(title="Linked Accounts", description=s, color=embedcolor)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def ov(ctx, *, bgname):
    bgname = bgname.lower()
    bgdat = bot.bgdata.get(bgname)
    if bgdat is None:
        return await ctx.reply(f"Background `{bgname}` not found!")
    if bgdat["ov"]:
        bgdat["ov"] = False
    else:
        bgdat["ov"] = True

    bot.bgdata[bgname] = bgdat
    await savebgdata()
    await ctx.message.add_reaction(economysuccess)

@bot.command()
@commands.check(general)
async def help(ctx, specify=None):
    embed = discord.Embed(color=embedcolor,
                          description=f'To get help on a command, use `v.help <command name>`')
    embed.set_author(name='Help')
    embed.set_footer(text='Bot developed by AwesomeSam#7985', icon_url=sampfp)
    if specify is None:
        for j in bot.help_json:
            mylist = []
            max_l = 0
            for i in bot.help_json[j].keys():
                if i == "category": continue
                info = bot.help_json[j][i]['usage']
                print(info)
                cmdl = len(info.split(' ')[0])
                if cmdl > max_l:
                    max_l = cmdl
                mylist.append(info)
            finallist = []
            for cmds in mylist:
                splitted = cmds.split(' ')
                first = splitted[0]
                first = first + ' '*(max_l-len(first))
                splitted.pop(0)
                splitted.insert(0, first)
                finallist.append(' '.join(splitted))
            content = '\n'.join(finallist)
            embed.add_field(name=f'**● __{j}__**', value=f'```less\n{content}```', inline=False)
        embed.add_field(name='\u200b', value=f'`<>` and `[]` are **not** required while using commands\n\n'
                                             f'Syntax: `<>` = Required `[]` = Optional')
        try:
            await ctx.author.send(embed=embed)
            embed = discord.Embed(title=f'{economysuccess} You received a mail!', color=success_embed)
            await ctx.reply(embed=embed)
        except:
            await ctx.send(embed=embed)
        return
    x = bot.help_json.values()
    notfound = True
    for i in x:
        for j in i.keys():
            if j == 'category':
                continue
            available = []
            available.append(j[2:])
            info = i[j]

            for k in info['aliases']:
                available.append(k)
            if specify.lower() in available:
                alias_list = [f'{q}' for q in info['aliases']]

                for aliases in alias_list:
                    if aliases[0:2] != 'v.':
                        if aliases == 'None': continue
                        alias_list.remove(aliases)
                        aliases = 'v.' + aliases
                        alias_list.insert(0, aliases)
                embed = discord.Embed(color=embedcolor, title=f'Command: {j[2:]}', description=info['desc']+f'\n\n**Category:** `{i["category"]}`\n**Usage:** `{info["usage"]}`')
                embed.add_field(name='Aliases', value='```less\n'+'\n'.join(alias_list)+'```', inline=False)
                embed.set_footer(text='Syntax: <> = required, [] = optional')
                notfound = False
                await ctx.send(embed=embed)
                break
    if notfound:
        embed = discord.Embed(description=f'{economyerror} No help found or command doesn\'t exist!', color=error_embed)
        await ctx.send(embed=embed)

@bot.command(aliases=['add_chl'])
@commands.check(general)
async def set_chl(ctx, channel:discord.TextChannel):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_channels or ctx.author.id in devs: pass
    else: return
    server = await get_admin()
    if channel.id in server:
        embed = discord.Embed(description=f'{economyerror} {channel.mention} is already in list of registered channels!', color=error_embed)
        return await ctx.send(embed=embed)
    server.append(channel.id)
    if ctx.channel.id not in server:
        server.append(ctx.channel.id)
    await close_admin(server)
    embed = discord.Embed(description=f'{economysuccess} {channel.mention} added to list of registered channels successfully!', color=success_embed)
    await ctx.send(embed=embed)

@bot.command(aliases=['rem_chl', 'remove_chl', 'delete_chl'])
@commands.check(general)
async def del_chl(ctx, channel:discord.TextChannel):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_channels or ctx.author.id in devs: pass
    else: return
    server = await get_admin()
    if channel.id not in server:
        embed = discord.Embed(description=f'{economyerror} {channel.mention} not in list of registered channels!', color=error_embed)
        return await ctx.send(embed=embed)
    server.remove(channel.id)
    await close_admin(server)
    embed = discord.Embed(description=f'{economysuccess} {channel.mention} removed from list of registered channels successfully!', color=success_embed)
    await ctx.send(embed=embed)

@bot.command(aliases=['show_chl'])
@commands.check(general)
async def list_chl(ctx):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_channels or ctx.author.id in devs: pass
    else: return
    server = await get_admin()
    if len(server) == 0: channels = ['> No channels set']
    else: channels = [f'> <#{x}>' for x in server]
    embed = discord.Embed(title=f'{economysuccess} Allowed Channels for the bot:', description='\n'.join(channels), color=embedcolor)
    embed.set_footer(text='Add a channel using v.set_chl <name>\nRemove a channel using v.del_chl <name>')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(general)
async def reset_chl(ctx):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_channels or ctx.author.id in devs: pass
    else: return
    server = await get_admin()
    embed = discord.Embed(title=f'{economysuccess} Done', description='Cleared Successfully!', color=embedcolor)
    await close_admin(server)
    embed.set_footer(text='Add a channel using e.set_chl <name>\nRemove a channel using e.del_chl <name>')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(general)
async def ping(ctx):
    msg = await ctx.send('Pong!')
    ping = "{:.2f}".format(bot.latency*1000)
    await msg.edit(content=f'Pong! `{ping} ms`')

@bot.command()
@commands.is_owner()
async def load_peeps(ctx=None):
    a = requests.get("https://kr.vercel.app/api/clan?clan=vnta")
    data = json.loads(a.text)
    bot.vntapeeps.clear()
    for i in data["data"]["members"]:
        bot.vntapeeps.append(i["username"].lower())

@bot.command(aliases=["ref"])
async def load_data(ctx=None):
    chl = bot.get_channel(854692793276170280)
    msgs = await chl.history(limit=1).flatten()
    bot.refr = json.loads(msgs[0].content)

    chl = bot.get_channel(854721559359913994)
    msgs = await chl.history(limit=1).flatten()
    bot.links.update(json.loads(requests.get(msgs[0].attachments[0]).text))
    bot.dev = await bot.fetch_user(771601176155783198)

    chl = bot.get_channel(856070919033978932)
    msgs = await chl.history(limit=1).flatten()
    bot.userdata = json.loads(requests.get(msgs[0].attachments[0]).text)

    chl = bot.get_channel(854698116255318057)
    msgs = await chl.history(limit=1).flatten()
    bot.bgdata = json.loads(requests.get(msgs[0].attachments[0]).text)

@bot.event
async def on_connect():
    print("Connected")
    await bot.wait_until_ready()
    await load_data()
    await load_peeps()
    print("Ready")
    if not bot.pause or not bot.beta:
        if not bot.cwpause: asyncio.create_task(auto_update())

@bot.event
async def on_message(message):
    if bot.beta:
        if message.channel.id != 854008993248051230: return
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == 853971223682482226: return
    if str(payload.emoji) == "🗑️" and payload.user_id == 771601176155783198:
        chl = await bot.fetch_channel(payload.channel_id)
        msg = await chl.fetch_message(payload.message_id)
        await msg.delete()
    if payload.channel_id == 855450311808122951 and str(payload.emoji) in ["✅", "❌"]:

        if str(payload.emoji) == "❌":
            userd = bot.pendings[payload.message_id]
            user = userd[0]
            user = await bot.fetch_user(user)
            await user.send(f"❌ Your request to link with `{userd[1]}` is denied!")
            state= "Denied"
        else:
            userd = bot.pendings[payload.message_id]
            user = userd[0]
            user = await bot.fetch_user(user)
            t = bot.links.get(str(user.id), {"main":userd[1], "all":[]})
            t["all"] = list(set(t["all"]))
            if userd[1] in t["all"]:
                return await user.send(f"You are already linked with `{userd[1]}`")
            t["all"].append(userd[1])
            bot.links[str(user.id)] = t
            state= "Accepted"
            await update_links()
            await user.send(f"✅ Your request to link with `{userd[1]}` is accepted!")
        bot.pendings.pop(payload.message_id)
        chl = bot.get_channel(payload.channel_id)
        msg = await chl.fetch_message(payload.message_id)
        await msg.edit(content=f"{msg.content} (`{state}` by {await bot.fetch_user(payload.user_id)})")
        await msg.clear_reactions()

#@bot.event
async def on_command_error(ctx, error):
    pass

bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")
