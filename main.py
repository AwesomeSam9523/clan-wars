import asyncio, discord, json, sys, random, copy, aiohttp, traceback
import time, datetime, os, threading, requests, psutil, functools, numexpr
from prettytable import PrettyTable
from discord.ext import commands, tasks
from discord.ext.commands import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageSequence, ImageColor
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from typing import Union

print("Starting")
intents = discord.Intents.default()
intents.members = True
class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=["V.", "v."], case_insensitive=True, intents=intents)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(PersistentView())
            self.persistent_views_added = True

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Pubstomper", custom_id="pubs_3",
                              emoji="<:ak:861873538134573056>")
    async def pubsb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await pubs(interaction)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Competitive", custom_id="comp_3",
                              emoji="<:smg:861873439421235220>")
    async def compb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await comp(interaction)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Content Creation", custom_id="cc_3",
                              emoji="<:trooper:861873482576953385>")
    async def ccb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await cc(interaction)

YT_API_KEY = "AIzaSyDB4zCQQ54G31iA4Cs-AXmWJnm1iSP7Lgw"
SOCIAL_KEYS = ["AIzaSyC6Zaibw8jVcxT42yhGRnSLl-fui334bT0", "AIzaSyAf4hSXUzCSXoxpZQFRypr-8VEVdexCapo", "AIzaSyDYIs60oDoXXmtAqD50Zxh_ZQdYcONIoc0"]
CLIENT_ID = "0dgqs0ani15dwgr1pn8ojbbvvn81k8"
CLIENT_SECRET = "20k31xx6rnzkqf1vqim843eopd7e24"

TWITTER_API_KEY = "nm6dTe6hT07TgOV6SFvtJHktc"
TWITTER_API_SECRET = "4s77OUIGgaB0j7T0xEs0KY9lVeIrcf75e2e17SOjFBt2xNWUaB"
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALRjRwEAAAAA8Jzs2fXphQlosXN2ewneKU4gNvQ%3D6dKHyQTzIOjXnKJbxs7ltt5XmFoArwXyMqUKCLOBJWpNe8IJEZ"

bot = PersistentViewBot()
bot.session = None
bot.apikey = YT_API_KEY
bot.remove_command("help")
bot.loop.set_debug(True)
bot.loop.slow_callback_duration = 1
bot.refr = {}
bot.twitchapi = {"expiry":0}
bot.links = {}
bot.userdata = {}
bot.bgdata = {}
bot.unsaved = {}
bot.cache = {}
bot.pendings = {}
bot.already = []
bot.vntapeeps = []
bot.excl = [671436261482823763, "oof*100"]
bot.dcmds = []
bot.dev = bot.get_user(771601176155783198)
bot.linkinglogs = bot.get_channel(861463678179999784)
bot.starboards = bot.get_channel(874717466134208612)
bot.interlist = []
bot.uptime = time.time()
bot.reqs = 0
bot.pause = False
bot.cwpause = True
allowdevs = False
bot.usage_ = True
if os.path.exists("C:"): bot.beta = True
else: bot.beta = False
bot.webworking = False
bot.apidown = False
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
    },
      "v.target":{
          "aliases":["tar"],
          "usage":"v.target <kills> [ign]",
          "desc":"Find the required KPG and KPM to achieve certain kills **from now**"
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
            "usage":"v.link <ign>",
            "desc":"Links your account to bot"
        },
        "v.unlink":{
            "aliases":["None"],
            "usage":"v.unlink <ign>",
            "desc":"Unlinks your account from bot"
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
    },
    "Utility":{
        "category":"Utility",
        "v.reminder":{
            "usage":"v.reminder",
            "desc":"Set/Delete a reminder",
            "aliases":["reminders", "rem", "rems"]
        },
        "v.remindme":{
            "usage":"v.remindme <time> [desc]",
            "desc":"Quick Reminder",
            "aliases":["None"]
        },
        "v.calculator":{
            "aliases":["c", "calc"],
            "desc":"Modern Calculator",
            "usage":"v.calc [equation]"
        },
        "v.post":{
            "aliases":["None"],
            "desc":"Post your settings, css, scope or any suggestion",
            "usage":"v.post"
        }
    },
    "Staff": {
        "category":"Staff",
        "v.appconfig": {
            "aliases": ["appc"],
            "usage": "v.appconfig",
            "desc": "Modify requirements",
        },
        "v.forcelink":{
            "aliases":["fl", "forcel", "flink"],
            "usage":"v.forcelink @user <ign>",
            "desc":"Force link a user with an account"
        },
        "v.set_chl": {
            "aliases": ["add_chl"],
            "usage": "v.set_chl <#channel>",
            "desc": "Allows the bot to respond in that channel",
        },
        "v.del_chl": {
            "aliases": ["delete_chl", "rem_chl", "remove_chl"],
            "usage": "v.del_chl <#channel>",
            "desc": "Disallows the bot to respond in that channel",
        },
        "v.list_chl": {
            "aliases": ["show_chl"],
            "usage": "v.list_chl",
            "desc": "Lists all the channels where the bot is allowed to respond",
        },
        "v.reset_chl": {
            "aliases": ["None"],
            "usage": "v.reset_chl",
            "desc": "Clears all the configuration and makes the bot to respond again in **all** the channels",
        }
    }
}
bot.ytcache = {}
warn1 = []
warn2 = []
devs = [771601176155783198]
staffchl = [854008993248051230, 813444187566506027]
flags_list = [['Afghanistan', 'af', 0], ['Albania', 'al', 1], ['Algeria', 'dz', 2], ['American Samoa', 'as', 3], ['Andorra', 'ad', 4], ['Angola', 'ao', 5], ['Anguilla', 'ai', 6], ['Antarctica', 'aq', 7], ['Antigua and Barbuda', 'ag', 8], ['Argentina', 'ar', 9], ['Armenia', 'am', 10], ['Aruba', 'aw', 11], ['Australia', 'au', 12], ['Austria', 'at', 13], ['Azerbaijan', 'az', 14], ['Bahamas', 'bs', 15], ['Bahrain', 'bh', 16], ['Bangladesh', 'bd', 17], ['Barbados', 'bb', 18], ['Belarus', 'by', 19], ['Belgium', 'be', 20], ['Belize', 'bz', 21], ['Benin', 'bj', 22], ['Bermuda', 'bm', 23], ['Bhutan', 'bt', 24], ['Bolivia', 'bo', 25], ['Bosnia and Herzegovina', 'ba', 26], ['Botswana', 'bw', 27], ['Brazil', 'br', 28], ['British Indian Ocean Territory', 'io', 29], ['British Virgin Islands', 'vg', 30], ['Brunei', 'bn', 31], ['Bulgaria', 'bg', 32], ['Burkina Faso', 'bf', 33], ['Burundi', 'bi', 34], ['Cambodia', 'kh', 35], ['Cameroon', 'cm', 36], ['Canada', 'ca', 37], ['Cape Verde', 'cv', 38], ['Cayman Islands', 'ky', 39], ['Central African Republic', 'cf', 40], ['Chad', 'td', 41], ['Chile', 'cl', 42], ['China', 'cn', 43], ['Christmas Island', 'cx', 44], ['Cocos Islands', 'cc', 45], ['Colombia', 'co', 46], ['Comoros', 'km', 47], ['Cook Islands', 'ck', 48], ['Costa Rica', 'cr', 49], ['Croatia', 'hr', 50], ['Cuba', 'cu', 51], ['Curacao', 'cw', 52], ['Cyprus', 'cy', 53], ['Czech Republic', 'cz', 54], ['Democratic Republic of the Congo', 'cd', 55], ['Denmark', 'dk', 56], ['Djibouti', 'dj', 57], ['Dominica', 'dm', 58], ['Dominican Republic', 'do', 59], ['East Timor', 'tl', 60], ['Ecuador', 'ec', 61], ['Egypt', 'eg', 62], ['El Salvador', 'sv', 63], ['Equatorial Guinea', 'gq', 64], ['Eritrea', 'er', 65], ['Estonia', 'ee', 66], ['Ethiopia', 'et', 67], ['Falkland Islands', 'fk', 68], ['Faroe Islands', 'fo', 69], ['Fiji', 'fj', 70], ['Finland', 'fi', 71], ['France', 'fr', 72], ['French Polynesia', 'pf', 73], ['Gabon', 'ga', 74], ['Gambia', 'gm', 75], ['Georgia', 'ge', 76], ['Germany', 'de', 77], ['Ghana', 'gh', 78], ['Gibraltar', 'gi', 79], ['Greece', 'gr', 80], ['Greenland', 'gl', 81], ['Grenada', 'gd', 82], ['Guam', 'gu', 83], ['Guatemala', 'gt', 84], ['Guernsey', 'gg', 85], ['Guinea', 'gn', 86], ['Guinea-Bissau', 'gw', 87], ['Guyana', 'gy', 88], ['Haiti', 'ht', 89], ['Honduras', 'hn', 90], ['Hong Kong', 'hk', 91], ['Hungary', 'hu', 92], ['Iceland', 'is', 93], ['India', 'in', 94], ['Indonesia', 'id', 95], ['Iran', 'ir', 96], ['Iraq', 'iq', 97], ['Ireland', 'ie', 98], ['Isle of Man', 'im', 99], ['Israel', 'il', 100], ['Italy', 'it', 101], ['Ivory Coast', 'ci', 102], ['Jamaica', 'jm', 103], ['Japan', 'jp', 104], ['Jersey', 'je', 105], ['Jordan', 'jo', 106], ['Kazakhstan', 'kz', 107], ['Kenya', 'ke', 108], ['Kiribati', 'ki', 109], ['Kosovo', 'xk', 110], ['Kuwait', 'kw', 111], ['Kyrgyzstan', 'kg', 112], ['Laos', 'la', 113], ['Latvia', 'lv', 114], ['Lebanon', 'lb', 115], ['Lesotho', 'ls', 116], ['Liberia', 'lr', 117], ['Libya', 'ly', 118], ['Liechtenstein', 'li', 119], ['Lithuania', 'lt', 120], ['Luxembourg', 'lu', 121], ['Macau', 'mo', 122], ['Macedonia', 'mk', 123], ['Madagascar', 'mg', 124], ['Malawi', 'mw', 125], ['Malaysia', 'my', 126], ['Maldives', 'mv', 127], ['Mali', 'ml', 128], ['Malta', 'mt', 129], ['Marshall Islands', 'mh', 130], ['Mauritania', 'mr', 131], ['Mauritius', 'mu', 132], ['Mayotte', 'yt', 133], ['Mexico', 'mx', 134], ['Micronesia', 'fm', 135], ['Moldova', 'md', 136], ['Monaco', 'mc', 137], ['Mongolia', 'mn', 138], ['Montenegro', 'me', 139], ['Montserrat', 'ms', 140], ['Morocco', 'ma', 141], ['Mozambique', 'mz', 142], ['Myanmar', 'mm', 143], ['Namibia', 'na', 144], ['Nauru', 'nr', 145], ['Nepal', 'np', 146], ['Netherlands', 'nl', 147], ['Netherlands Antilles', 'an', 148], ['New Caledonia', 'nc', 149], ['New Zealand', 'nz', 150], ['Nicaragua', 'ni', 151], ['Niger', 'ne', 152], ['Nigeria', 'ng', 153], ['Niue', 'nu', 154], ['North Korea', 'kp', 155], ['Northern Mariana Islands', 'mp', 156], ['Norway', 'no', 157], ['Oman', 'om', 158], ['Pakistan', 'pk', 159], ['Palau', 'pw', 160], ['Palestine', 'ps', 161], ['Panama', 'pa', 162], ['Papua New Guinea', 'pg', 163], ['Paraguay', 'py', 164], ['Peru', 'pe', 165], ['Philippines', 'ph', 166], ['Pitcairn', 'pn', 167], ['Poland', 'pl', 168], ['Portugal', 'pt', 169], ['Puerto Rico', 'pr', 170], ['Qatar', 'qa', 171], ['Republic of the Congo', 'cg', 172], ['Reunion', 're', 173], ['Romania', 'ro', 174], ['Russia', 'ru', 175], ['Rwanda', 'rw', 176], ['Saint Barthelemy', 'bl', 177], ['Saint Helena', 'sh', 178], ['Saint Kitts and Nevis', 'kn', 179], ['Saint Lucia', 'lc', 180], ['Saint Martin', 'mf', 181], ['Saint Pierre and Miquelon', 'pm', 182], ['Saint Vincent and the Grenadines', 'vc', 183], ['Samoa', 'ws', 184], ['San Marino', 'sm', 185], ['Sao Tome and Principe', 'st', 186], ['Saudi Arabia', 'sa', 187], ['Senegal', 'sn', 188], ['Serbia', 'rs', 189], ['Seychelles', 'sc', 190], ['Sierra Leone', 'sl', 191], ['Singapore', 'sg', 192], ['Sint Maarten', 'sx', 193], ['Slovakia', 'sk', 194], ['Slovenia', 'si', 195], ['Solomon Islands', 'sb', 196], ['Somalia', 'so', 197], ['South Africa', 'za', 198], ['South Korea', 'kr', 199], ['South Sudan', 'ss', 200], ['Spain', 'es', 201], ['Sri Lanka', 'lk', 202], ['Sudan', 'sd', 203], ['Suriname', 'sr', 204], ['Svalbard and Jan Mayen', 'sj', 205], ['Swaziland', 'sz', 206], ['Sweden', 'se', 207], ['Switzerland', 'ch', 208], ['Syria', 'sy', 209], ['Taiwan', 'tw', 210], ['Tajikistan', 'tj', 211], ['Tanzania', 'tz', 212], ['Thailand', 'th', 213], ['Togo', 'tg', 214], ['Tokelau', 'tk', 215], ['Tonga', 'to', 216], ['Trinidad and Tobago', 'tt', 217], ['Tunisia', 'tn', 218], ['Turkey', 'tr', 219], ['Turkmenistan', 'tm', 220], ['Turks and Caicos Islands', 'tc', 221], ['Tuvalu', 'tv', 222], ['U.S. Virgin Islands', 'vi', 223], ['Uganda', 'ug', 224], ['Ukraine', 'ua', 225], ['United Arab Emirates', 'ae', 226], ['United Kingdom', 'gb', 227], ['United States', 'us', 228], ['Uruguay', 'uy', 229], ['Uzbekistan', 'uz', 230], ['Vanuatu', 'vu', 231], ['Vatican', 'va', 232], ['Venezuela', 've', 233], ['Vietnam', 'vn', 234], ['Wallis and Futuna', 'wf', 235], ['Western Sahara', 'eh', 236], ['Yemen', 'ye', 237], ['Zambia', 'zm', 238], ['Zimbabwe', 'zw', 239]]
staff = []
accepted = [813786315530305536, 813527378088951809, 813527377736761384, 813452412810690600, 813441662588157952, 853997809212588073]
order = {813713185462681610: [814511339905089577, 813704960565837864, 813704961103888434, 813440705892057178,
                                  813440705497137212, 813441661806968878, 813440702788534303, 813439916842811433],
         813713007267676181: [823254966054420520, 813439915827658802, 813439922337087489, 813439922169970718,
                                  813439921440292917, 813439920873144330, 813452411825029160, 813441664025624646,
                                  835545980811870218, 840962503768670239, 850476873548300319, 814604370569330729,
                                  813527378088951809, 813527377736761384, 833377173477523476, 833377173975859221,
                                  844654018127331348, 844654478099742770],
         813441664919273473: [813452197966250024, 814161003041521725, 813452198344130570, 813452199270416445,
                                  813452411141619794, 813729487292334081],
         813713509804015677: [813713508487266401, 813713670537871390, 813713669417467925, 813713508360650794,
                                  813713671368343562, 813713508477960192, 813713671434797086, 813713668771938324,
                                  813713509586042880, 733161301748088895, 818500848526032916, 856108515059171328,
                                  867409936019357707, 860253758784405505, 860790673128423424, 867405643232182292,
                                  859458033876729856, 863797568126058527, 864001098490839040, 862974237609820170,
                                  855413544844394546, 867405814875291648, 852831111348224010, 857863855267250207,
                                  861102137923600384, 856022125139722291, 857702070568222781, 858737388049006602,
                                  864163763724484608, 854400768533331968, 857459053411303444, 852830517194784799,
                                  859275060790951966, 856994513914560552, 853714634280271883, 853482658138292236,
                                  853682026790780949, 856972592967188501, 853049609914941470, 836784812001591297,
                                  835782018968190996, 853234007167598653, 853336822327148594, 853271796061044766,
                                  866641487994945536, 852800177295327242, 853076127030837278, 858384194471723009,
                                  852798231167107123, 852813875615105065, 853282869346959400, 852794742161014794,
                                  852879710895472651, 852736622360920134, 836661337412075521, 844912463623094313,
                                  834346081428570162, 845561689768067092, 835513734570311680, 844586713644138536,
                                  823126696306802718, 834086293095972876, 836641820602662962, 835564323136995368,
                                  837232066973794336, 844215221982855208, 840842478717894686, 823571172426776626,
                                  819078762439901194, 848659609358434304, 855793126958170122],
         813713012564295701: [857525749875081226, 813439916125978664, 813441664617939004, 823303887430877224,
                                  820234763650465822, 819823118163509268, 813452412810690600, 823303541090549770,
                                  823303540365066262, 812034716373876818, 813439914356113438, 813439914862968842,
                                  813441662588157952, 819077019949727804]}
usercmds = {}
saycmd = {}
lastdata = {}

error_embed = 16730441
embedcolor = 5046208
success_embed = 5963593
localembed = 16734606
economyerror = "❌"
economysuccess = "✅"
loading = "<a:loading:862916076769378304>"
youtube = "<:YouTube:865575628710608916>"
twitch = "<:Twitch:865575682208825355>"
twitter = "<:Twitter:866566539581587456>"
color = 7929797
sampfp = "https://media.discordapp.net/attachments/854008993248051230/854708889059852288/sam_av.png"

@bot.check
async def if_allowed(ctx):
    if bot.apidown: await load_peeps()
    if bot.beta: return True
    if "ticket" in ctx.channel.name: return True
    else: return await check_channel(ctx.channel.id)

@bot.check
async def if_enabled(ctx):
    if ctx.command.name in bot.refr.setdefault("dcmds", {}).keys():
        if allowdevs: return True
        await ctx.reply("Command disabled at the moment.\n"
                        f"Reason: {bot.refr['dcmds'][ctx.command.name]}")
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
    bot.reqs += 1
    if time.time() - lastdata.setdefault(clan, {}).setdefault("time", 0) < 5:
        return lastdata[clan]["data"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kr.vercel.app/api/clan?clan={clan}", timeout=aiohttp.ClientTimeout(total=10)) as data:
                if data.status != 200:
                    return "error"
                res = json.loads(await data.text())
                lastdata[clan]["time"] = time.time()
                lastdata[clan]["data"] = res
                return res
    except: return "error"

async def embed_view(clan):
    data = await getdata(clan)
    if data == "error":
        return "error"
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
            active_con = discord.Embed(description=f"```css\n{active.get_string()[count:count+2000]}```",
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
            active_con = discord.Embed(description=f"```css\n{expired.get_string()[count:count+2000]}```",
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
    bot.refr["disregarded"].append(userid)
    await asyncio.sleep(10*60)
    bot.refr["disregarded"].remove(userid)

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

async def close_admin():
    chl = bot.get_channel(854692793276170280)
    with open("admin.json", "w") as f:
        f.write(json.dumps(bot.refr, indent=2))
    await chl.send(file=discord.File("admin.json"))

async def updateuserdata():
    chl = bot.get_channel(856070919033978932)
    with open("userdata.json", "w") as f:
        f.write(json.dumps(bot.userdata, indent=2))
    await chl.send(file=discord.File("userdata.json"))

async def checkuserclan(ign):
    clanlist = bot.refr.setdefault("userclans", {})

    for k, v in clanlist.items():
        print(k, v)
        if ign.lower() in v:
            return k
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
            userdata = json.loads(await data.text())
            clan = userdata["data"]["clan"]
            if clan == "": return "no"
            clandata = await getdata(clan)
            data2 = clandata["data"]["members"]
            found = False
            datafile = []
            for i in data2: datafile.append(i["username"].lower())
            clanlist[clan] = datafile
            bot.refr["userclans"] = clanlist
            return clan

@tasks.loop(minutes=5.0)
async def auto_update():
    await update_embeds("VNTA")

@tasks.loop(seconds=60)
async def yt_socials_check():
    reqs = bot.refr.get("api", 0)
    if reqs >= 2500:
        bot.apikey = SOCIAL_KEYS[0]
    elif reqs >= 12475:
        bot.apikey = SOCIAL_KEYS[1]
    elif reqs >= 22450:
        bot.apikey = SOCIAL_KEYS[2]
    else:
        bot.apikey = YT_API_KEY
        bot.refr['api'] = 0
    SOCIAL_KEY = bot.apikey
    for i in bot.refr["social_yt"]["subs"]:
        ytcache = bot.refr.setdefault("ytcache", {})
        uploadsid = ytcache.get(i)
        if uploadsid is None:
            uri = f"https://www.googleapis.com/youtube/v3/channels?id={i}&key={YT_API_KEY}&part=contentDetails"
            a = requests.get(uri)
            data = a.json()
            if data["pageInfo"]["totalResults"] == 0:
                bot.refr["social_yt"]["subs"].remove(i)
                continue
            uploadsid = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            ytcache[i] = uploadsid
        uri2 = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={uploadsid}&key={SOCIAL_KEY}"
        b = requests.get(uri2)
        print(b.headers)
        vids = b.json()
        if vids.get('error'):
            err = vids['error']
            print(err)
            try:
                print(SOCIAL_KEYS.index(bot.apikey))
            except:
                print('YT_API_KEY')
            if err['code'] == 403:
                '''
                await bot.get_channel(867264621211156500).send(
                    f'<@771601176155783198> YT API Quota Exceeded.\n' + 
                    f'Reqs: {reqs}.'
                )'''
                if reqs >= 22450:
                    reqs = 0
                elif reqs >= 12475:
                    reqs = 22450
                elif reqs >= 2500:
                    reqs = 12475
                else:
                    reqs = 2500
                bot.refr['api'] = reqs
                return
        vidid = vids["items"][0]["contentDetails"]["videoId"]
        print(vidid)
        print('\n-----------------\n')
        donevids = bot.refr.setdefault("ytdone", [])
        if vidid not in donevids:
            firstcheck = bot.refr.setdefault("ytfirst", [])
            if i in firstcheck:
                await newvideo(vidid, vids["items"][0]["snippet"]["channelTitle"])
            else:
                firstcheck.append(i)
                donevids.append(vidid)
        bot.refr['api'] += 1
    print('\n\n====================\n\n')
    await close_admin()

@tasks.loop(seconds=40)
async def twitch_socials_check():
    if bot.twitchapi["expiry"] < time.time():
        print("Requesting new token...")
        a = requests.post(
            f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")
        res = json.loads(a.text)
        bot.twitchapi["token"] = res["access_token"]
        bot.twitchapi["expiry"] = time.time() + res["expires_in"]
    header = {'Authorization': f'Bearer {bot.twitchapi["token"]}', 'Client-Id': CLIENT_ID}
    for i in bot.refr["social_twitch"]["subs"]:
        uri = f"https://api.twitch.tv/helix/streams?user_login={i}"
        a = requests.get(uri, headers=header)
        data = json.loads(a.text)
        fin = data.get("data", [])
        checklist = bot.refr.setdefault("twitchlive", [])
        if len(fin) != 0:
            if i in checklist: continue
            checklist.append(i)
            await streamstart(fin[0])
        else:
            if i in checklist: checklist.remove(i)
            continue

@tasks.loop(seconds=20)
async def twitter_socials_check():
    header = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    for k, i in bot.refr["social_twitter"]["subs"].items():
        uri = f"https://api.twitter.com/2/users/{i}/tweets"
        a = requests.get(uri, headers=header)
        data = json.loads(a.text)
        data = data["data"][0]
        donetweets = bot.refr.setdefault("twitterdone", [])
        firstcheck = bot.refr.setdefault("twitterfirst", [])
        if data['id'] not in donetweets:
            if i in firstcheck:
                await newtweet(k, data)
            else:
                firstcheck.append(i)
                donetweets.append(data['id'])

async def newvideo(vidid, name):
    ytdata = bot.refr["social_yt"]
    chl = bot.get_channel(ytdata["channel"])
    if name == "VNTA Krunker":
        role = chl.guild.get_role(ytdata["role"]).mention
    else: 
        role = "Hey All!"
    await chl.send(ytdata["msg"].format(name=name, role=role, link=f"https://youtu.be/{vidid}"))
    donevids = bot.refr["ytdone"]
    donevids.append(vidid)
    bot.refr["ytdone"] = donevids
    await close_admin()

async def streamstart(data):
    ytdata = bot.refr["social_twitch"]
    chl = bot.get_channel(ytdata["channel"])
    role = chl.guild.get_role(ytdata["role"])
    await chl.send(ytdata["msg"].format(name=data["user_name"],
                                        role=role.mention,
                                        link=f"https://twitch.tv/{data['user_login']}",
                                        title=data['title']))

async def newtweet(user, data):
    ytdata = bot.refr["social_twitter"]
    chl = bot.get_channel(ytdata["channel"])
    role = chl.guild.get_role(ytdata["role"])
    twmsg = ytdata["msg"].format(name=user, role=role.mention, link=f"https://twitter.com/i/web/status/{data['id']}")
    await chl.send(twmsg)
    donevids = bot.refr["twitterdone"]
    donevids.append(data['id'])
    bot.refr["twitterdone"] = donevids
    await close_admin()

facts = ("Most American car horns honk in the key of F.",
    "The name Wendy was made up for the book 'Peter Pan.'",
    "Barbie's full name is Barbara Millicent Roberts.",
    "Every time you lick a stamp, you consume 1/10 of a calorie.",
    "The average person falls asleep in seven minutes.",
    "Studies show that if a cat falls off the seventh floor of a building it has about thirty percent less chance of surviving than a cat that falls off the twentieth floor. It supposedly takes about eight floors for the cat to realize what is occurring, relax and correct itself.",
    "Your stomach has to produce a new layer of mucus every 2 weeks otherwise it will digest itself.",
    "The citrus soda 7-UP was created in 1929; '7' was selected after the original 7-ounce containers and 'UP' for the direction of the bubbles.",
    "101 Dalmatians, Peter Pan, Lady and the Tramp, and Mulan are the only Disney cartoons where both parents are present and don't die throughout the movie.",
    "A pig's orgasm lasts for 30 minutes.",
    "'Stewardesses' is the longest word that is typed with only the left hand.",
    "To escape the grip of a crocodile's jaws, push your thumbs into its eyeballs - it will let you go instantly.",
    "Reindeer like to eat bananas.",
    "No word in the English language rhymes with month, orange, silver and purple.",
    "The word 'samba' means 'to rub navels together.'",
    "Mel Blanc (the voice of Bugs Bunny) was allergic to carrots.",
    "The electric chair was invented by a dentist.",
    "The very first bomb dropped by the Allies on Berlin during World War II Killed the only elephant in the Berlin Zoo.",
    "More people are killed annually by donkeys than airplane crashes.",
    "A 'jiffy' is a unit of time for 1/100th of a second.", "A whale's penis is called a dork.",
    "Because of the rotation of the earth, an object can be thrown farther if it is thrown west.",
    "The average person spends 6 months of their life sitting at red lights.",
    "In 1912 a law passed in Nebraska where drivers in the country at night were required to stop every 150 yards, send up a skyrocket, wait eight minutes for the road to clear before proceeding cautiously, all the while blowing their horn and shooting off flares.",
    "More Monopoly money is printed in a year, than real money throughout the world.",
    "Caesar salad has nothing to do with any of the Caesars. It was first concocted in a bar in Tijuana, Mexico, in the 1920's.",
    "One quarter of the bones in your body are in your feet.",
    "Crocodiles and alligators are surprisingly fast on land.  Although they are rapid, they are not agile.  So, if being chased by one, run in a zigzag line to lose him or her.",
    "Seattle’s Fremont Bridge rises up and down more than any drawbridge in the world.",
    "Right-handed people live, on average; nine years longer than left handed people.",
    "Ten percent of the Russian government's income comes from the sale of vodka.",
    "In the United States, a pound of potato chips costs two hundred times more than a pound of potatoes.",
    "A giraffe can go without water longer than a camel.",
    "A person cannot taste food unless it is mixed with saliva. For example, if a strong-tasting substance like salt is placed on a dry tongue, the taste buds will not be able to taste it. As soon as a drop of saliva is added and the salt is dissolved, however, a definite taste sensation results. This is true for all foods.",
    "Nearly 80% of all animals on earth have six legs.",
    "In the marriage ceremony of the ancient Inca Indians of Peru, the couple was considered officially wed when they took off their sandals and handed them to each other.",
    "Ninety percent of all species that have become extinct have been birds.",
    "There is approximately one chicken for every human being in the world.",
    "Most collect calls are made on father's day.",
    "The first automobile race ever seen in the United States was held in Chicago in 1895. The track ran from Chicago to Evanston, Illinois. The winner was J. Frank Duryea, whose average speed was 71/2 miles per hour.",
    "Each of us generates about 3.5 pounds of rubbish a day, most of it paper.",
    "Women manage the money and pay the bills in  75% of all Americans households.",
    "A rainbow can be seen only in the morning or late afternoon. It can occur only when the sun is 40 degrees or less above the horizon.",
    "It has NEVER rained in Calama, a town in the Atacama Desert of Chile.",
    "It costs more to buy a new car today in the United States than it cost Christopher Columbus to equip and undertake three voyages to and from the New World.",
    "The plastic things on the end of shoelaces are called aglets.",
    "An eighteenth-century German named Matthew Birchinger, known as 'the little man of Nuremberg,' played four musical instruments including the bagpipes, was an expert calligrapher, and was the most famous stage magician of his day. He performed tricks with the cup and balls that have never been explained. Yet Birchinger had no hands, legs, or thighs, and was less than 29 inches tall.",
    "Daylight Saving Time is not observed in most of the state of Arizona and parts of Indiana.",
    "Ants closely resemble human manners:  When they wake, they stretch & appear to yawn in a human manner before taking up the tasks of the day.",
    "Bees have 5 eyes. There are 3 small eyes on the top of a bee's head and 2 larger ones in front.",
    "Count the number of cricket chirps in a 15-second period, add 37 to the total, and your result will be very close to the actual outdoor Fahrenheit temperature.",
    "One-fourth of the world's population lives on less than $200 a year.  Ninety million people survive on less than $75 a year.",
    "Butterflies taste with their hind feet.",
    "Only female mosquito’s' bite and most are attracted to the color blue twice as much as to any other color.",
    "If one places a tiny amount of liquor on a scorpion, it will instantly go mad and sting itself to death.",
    "It is illegal to hunt camels in the state of Arizona.",
    "In eighteenth-century English gambling dens, there was an employee whose only job was to swallow the dice if there was a police raid.",
    "There are no clocks in Las Vegas gambling casinos.",
    "The human tongue tastes bitter things with the taste buds toward the back. Salty and pungent flavors are tasted in the middle of the tongue, sweet flavors at the tip!",
    "The first product to have a bar code was Wrigley’s gum.",
    "When you sneeze, air and particles travel through the nostrils at speeds over100 mph.  During this time, all bodily functions stop, including your heart, contributing to the impossibility of keeping one's eyes open during a sneeze.",
    "Annual growth of WWW traffic is 314,000%",
    "%60 of all people using the Internet, use it for pornography.",
    "In 1778, fashionable women of Paris never went out in blustery weather without a lightning rod attached to their hats.",
    "Sex burns 360 calories per hour.",
    "A raisin dropped in a glass of fresh champagne will bounce up and down continually from the bottom of the glass to the top.",
    "Celery has negative calories! It takes more calories to eat a piece of celery than the celery has in it.",
    "The average lead pencil will draw a line 35 miles long or write approximately 50,000 English words.  More than 2 billion pencils are manufactured each year in the United States. If these were laid end to end they would circle the world nine times.",
    "The pop you hear when you crack your knuckles is actually a bubble of gas burning.",
    "A literal translation of a standard traffic sign in China: 'Give large space to the festive dog that makes sport in the roadway.'",
    "You burn more calories sleeping than you do watching TV.",
    "Larry Lewis ran the 100-yard dash in 17.8 seconds in 1969, thereby setting a new world's record for runners in the 100-years-or-older class. He was 101.",
    "In a lifetime the average human produces enough quarts of spit to fill 2 swimming pools.",
    "It's against the law to doze off under a hair dryer in Florida/against the law to slap an old friend on the back in Georgia/against the law to Play hopscotch on a Sunday in Missouri.",
    "Barbie's measurements, if she were life-size, would be 39-29-33.",
    "The human heart creates enough pressure to squirt blood 30ft.",
    "One third of all cancers are sun related.",
    "THE MOST UNUSUAL CANNONBALL: On two occasions, Miss 'Rita Thunderbird' remained inside the cannon despite a lot of gunpowder encouragement to do otherwise. She performed in a gold lamé bikini and on one of the two occasions (1977) Miss Thunderbird remained lodged in the cannon, while her bra was shot across the Thames River.",
    "It has been estimated that humans use only 10% of their brain.",
    "Valentine Tapley from Pike County, Missouri  grew chin whiskers attaining a length of twelve feet six inches from 1860 until his death 1910, protesting Abraham Lincoln's election to the presidency.",
    "Most Egyptians died by the time they were 30 about 300 years ago,",
    "For some time Frederic Chopin, the composer and pianist, wore a beard on only one side of his face, explaining: 'It does not matter, my audience sees only my right side.'",
    "1 in every 4 Americans has appeared someway or another on television.",
    "1 in 8 Americans has worked at a McDonalds restaurant.",
    "70% of all boats sold are used for fishing.",
    "Studies have shown that children laugh an average of 300 times/day and adults 17 times/day, making the average child more optimistic, curious, and creative than the adult.",
    "A pregnant goldfish is called a twit.",
    "The shortest war in history was between Zanzibar and England in 1896. Zanzibar surrendered after 38 minutes.",
    "You were born with 300 bones, but by the time you are an adult you will only have 206.",
    "If you go blind in one eye you only lose about one fifth of your vision but all your sense of depth.",
    "Women blink nearly twice as much as men.",
    "The strongest muscle (Relative to size) in the body is the tongue.",
    "A Boeing 747's wingspan is longer than the Wright brother's first flight.",
    "American Airlines saved $40,000 in 1987 by eliminating one olive from each salad served in first-class.",
    "Average life span of a major league baseball: 7 pitches.",
    "A palindrome is a sentence or group of sentences that reads the same backwards as it does forward: Ex:  'Red rum, sir, is murder.' 'Ma is as selfless as I am.' 'Nurse, I spy gypsies. Run!'  'A man, a plan, a canal - Panama.' 'He lived as a devil, eh?'",
    "The first CD pressed in the US was Bruce Springsteen's 'Born in the USA'",
    "In 1986 Congress & President Ronald Reagan signed Public Law 99-359, which changed Daylight Saving Time from the last Sunday in April to the first Sunday in April.  It was estimated to save the nation about 300,000 barrels of oil each year by adding most of the month April to D.S.T.",
    "The thumbnail grows the slowest, the middle nail the fastest, nearly 4 times faster than toenails.",
    "The Human eyes never grow, but nose and ears never stop growing.",
    "The 57 on Heinz ketchup bottles represents the number of varieties of pickles the company once had.",
    "Tom Sawyer was the first novel written on a typewriter.",
    "If Texas were a country, its GNP would be the fifth largest of any country in the world.",
    "<@!771601176155783198> is GameBot Admin now B)",
    "There are 1 million ants for every human in the world.",
    "Odds of being killed by lightening? 1 in 2million/killed in a car crash? 1 in 5,000/killed by falling out of bed? 1 in 2million/killed in a plane crash? 1 in 25 million.",
    "Since 1978, 37 people have died by Vending Machine's falling on them.  13 people are killed annually.  All this while trying to shake merchandise out of them. 113 people have been injured.",
    "Half the foods eaten throughout the world today were developed by farmers in the Andes Mountains (including potatoes, maize, sweet potatoes, squash, all varieties of beans, peanuts, manioc, papayas, strawberries, mulberries and many others).",
    "The 'Golden Arches' of fast food chain McDonalds is more recognized worldwide than the religious cross of Christianity.",
    "Former basketball superstar Michael Jordan is the most recognized face in the world, more than the pope himself.",
    "The average talker sprays about 300 microscopic saliva droplets per minute, about 2.5 droplets per word.",
    "The Earth experiences 50,000 Earth quakes per year and is hit by Lightning 100 times a second.",
    "Every year 11,000 Americans injure themselves while trying out bizarre sexual positions.",
    "If we had the same mortality rate now as in 1900, more than half the people in the world today would not be alive.",
    "On average, Americans eat 18 acres of pizza everyday.",
    "Researchers at the Texas Department of Highways in Fort Worth determined the cow population of the U.S. burps some 50 million tons of valuable hydrocarbons into the atmosphere each year.  The accumulated burps of ten average cows could keep a small house adequately heated and its stove operating for a year.",
    "During a severe windstorm or rainstorm the Empire State Building sways several feet to either side.",
    "In the last 3,500 years, there have been approximately 230 years of peace throughout the civilized world.",
    "The Black Death reduced the population of Europe by one third in the period from 1347 to 1351.",
    "The average person spends about two years on the phone in a lifetime.",
    "Length of beard an average man would grow if he never shaved 27.5 feet",
    "Over 60% of all those who marry get divorced.", "400-quarter pounders can be made from 1 cow.",
    "A full-loaded supertanker traveling at normal speed takes at least 20 minutes to stop.",
    "Coca-Cola was originally green.", "Men can read smaller print than women; women can hear better.",
    "Hong Kong holds the most Rolls Royce’s per capita.",
    "Average number of days a West German goes without washing his underwear: 7",
    "WWII fighter pilots in the South Pacific armed their airplanes while stationed with .50 caliber machine gun ammo belts measuring 27 feet before being loaded into the fuselage. If the pilots fired all their ammo at a target, he went through 'the whole 9 yards', hence the term.",
    "Average number of people airborne over the US any given hour: 61,000.",
    "Intelligent people have more zinc and copper in their hair.",
    "Iceland consumes more Coca-Cola per capita than any other nation.",
    "In the early 1940s, the FCC assigned television's Channel 1 to mobile services (like two-way radios in taxis) but did not re-number the other channel assignments.",
    "The San Francisco Cable cars are the only mobile National Monuments.",
    "Firehouses have circular stairways originating from the old days when the engines were pulled by horses. The horses were stabled on the ground floor and figured out how to walk up straight staircases.",
    "The Main Library at Indiana University sinks over an inch every year because when it was built, engineers failed to take into account the weight of all the books that would occupy the building.",
    "111,111,111 x 111,111,111 = 12,345,678,987,654,321",
    "Statues in parks: If the horse has both front legs in the air, the person died in battle; if the horse has one front leg in the air, the person died as a result of wounds received in battle; if the horse has all four legs on the ground, the person died of natural causes.",
    "The expression 'to get fired' comes from long ago Clans that wanted to get rid of unwanted people, so they would burn their houses instead of killing them, creating the term 'Got fired'.",
    "'I am.' is the shortest complete sentence in the English language.",
    "Hershey's Kisses are called that because the machine that makes them looks like it's kissing the conveyor belt.",
    "The phrase 'rule of thumb' is derived from an old English law, which stated that you couldn't beat your wife with anything wider than your thumb.",
    "The longest recorded flight of a chicken is thirteen seconds.",
    "The Eisenhower interstate system requires that one mile in every five must be straight in case of war or emergency, they could be used as airstrips.",
    "The name Jeep came from the abbreviation used in the army. G.P. for 'General Purpose' vehicle.",
    "The Pentagon, in Arlington, Virginia, has twice as many bathrooms as is necessary, because when it was built in the 1940s, the state of Virginia still had segregation laws requiring separate toilet facilities for blacks and whites.",
    "The cruise liner, Queen Elizabeth II, moves only six inches for each gallon of diesel that it burns.",
    "If you have three quarters, four dimes, and four pennies, you have $1.19, the largest amount of money in coins without being able to make change for a dollar.",
    "In Aspen Colorado, you can have a maximum income of $104,000 and still receive government subsidized housing.",
    "Honking of car horns for a couple that just got married is an old superstition to insure great sex.",
    "Dr. Kellogg introduced Kellogg's Corn Flakes in hopes that it would reduce masturbation.",
    "The sperm of a mouse is actually longer than the sperm of an elephant.",
    "In medieval France, unfaithful wives were made to chase a chicken through town naked.",
    "The Black Widow spider eats her mate during or after sex.",
    "Napoleon's penis was sold to an American Urologist for $40,000.",
    "Eating the heart of a male Partridge was the cure for impotence in ancient Babylon.",
    "A bull can inseminate 300 cows from one single ejaculation.",
    "When a Hawaiian woman wears a flower over her left ear, it means that she is not available.",
    "The 'save' icon on Microsoft Word shows a floppy disk with the shutter on backwards.",
    "The only nation whose name begins with an 'A', but doesn't end in an 'A' is Afghanistan.",
    "The following sentence: 'A rough-coated, dough-faced, thoughtful ploughman strode through the streets of Scarborough; after falling into a slough, he coughed and hiccoughed.' Contains the nine different pronunciations of 'ough' in the English Language.",
    "The verb 'cleave' is the only English word with two synonyms which are antonyms of each other: adhere and separate.",
    "The only 15-letter word that can be spelled without repeating a letter is uncopyrightable.",
    "The shape of plant collenchyma’s cells and the shape of the bubbles in beer foam are the same - they are orthotetrachidecahedrons.",
    "Emus and kangaroos cannot walk backwards, and are on the Australian coat of arms for that reason.",
    "Cats have over one hundred vocal sounds, while dogs only have about ten.",
    "Blueberry Jelly Bellies were created especially for Ronald Reagan.",
    "PEZ candy even comes in a Coffee flavor.",
    "The first song played on Armed Forces Radio during operation Desert Shield was 'Rock the Casba' by the Clash.",
    "Non-dairy creamer is flammable.",
    "The airplane Buddy Holly died in was the 'American Pie.' (Thus the name of the Don McLean song.)",
    "Each king in a deck of playing cards represents a great king from history. Spades - King David, Clubs - Alexander the Great, Hearts - Charlemagne, and Diamonds - Julius Caesar.",
    "Golf courses cover 4% of North America.",
    "The average person will accidentally eat just under a pound of insects every year.",
    "Until 1994, world maps and globes sold in Albania only had Albania on them.",
    "The value of Pi will be officially 'rounded down' to 3.14 from 3.14159265359 on December 31, 1999.",
    "The Great Wall of China is the only man-made structure visible from space.",
    "A piece of paper can be folded no more then 9 times.",
    "The amount of computer Memory required to run WordPerfect for Win95 is 8 times the amount needed aboard the space shuttle.",
    "The average North American will eat 35,000 cookies during their life span.",
    "Between 25% and 33% of the population sneeze when exposed to light.",
    "The most common name in world is Mohammed.",
    "A guy named <@504029508295196683> is giga sus.",
    "Mount Olympus Mons on Mars is three times the size of Mount Everest.",
    "Most toilets flush in E flat.",
    "<@932930085646909481> is now verified in Krunker 😎",
    "2,000 pounds of space dust and other space debris fall on the Earth every day.",
    "Each month, there is at least one report of UFOs from each province of Canada.",
    "40,000 Americans are injured by toilets each year.",
    "You can be fined up to $1,000 for whistling on Sunday in Salt Lake City, Utah.",
    "It takes about 142.18 licks to reach the center of a Tootsie pop.",
    "The serial number of the first MAC ever produced was 2001.",
    "It is illegal to eat oranges while bathing in California.",
    "If done perfectly, a rubix cube combination can be solved in 17 turns.",
    "The average American butt is 14.9 inches long.",
    "More bullets were fired in 'Starship Troopers' than any other movie ever made.",
    "60% of electrocutions occur while talking on the telephone during a thunderstorm.",
    "The name of the girl on the statue of liberty is Mother of Exiles.",
    "3.6 cans of Spam are consumed each second.",
    "There's a systematic lull in conversation every 7 minutes.",
    "The buzz from an electric razor in America plays in the key of B flat; Key of G in England.",
    "There are 1,575 steps from the ground floor to the top of the Empire State building.",
    "The world's record for keeping a Lifesaver in the mouth with the hole intact is 7 hrs 10 min.",
    "There are 293 ways to make change for a dollar.",
    "The world record for spitting a watermelon seed is 65 feet 4 inches.",
    "In the Philippine jungle, the yo-yo was first used as a weapon.",
    "Dueling is legal in Paraguay as long as both parties are registered blood donors.",
    "Texas is also the only state that is allowed to fly its state flag at the same height as the U.S. flag.",
    "The three most recognized Western names in China are Jesus Christ, Richard Nixon, & Elvis Presley.",
    "There is a town in Newfoundland, Canada called Dildo.",
    "The Boston University Bridge (on Commonwealth Avenue, Boston, Massachusetts) is the only place in the world where a boat can sail under a train driving under a car driving under an airplane.",
    "All 50 states are listed across the top of the Lincoln Memorial on the back of the $5 bill.",
    "In space, astronauts are unable to cry, because there is no gravity and the tears won't flow.",
    "Chewing gum while peeling onions will keep you from crying.",
    "There are more plastic flamingos in the U.S that there are real ones.",
    "The crack of a whip is actually a tiny sonic boom, since the tip breaks the sound barrier.",
    "Jupiter is bigger than all the other planets in our solar system combined.",
    "Hot water is heavier than cold.",
    "The common idea that only 10% of the brain is used it not true as it is impossible to determine the actual percentage because of the complexity of the brain.",
    "Lawn darts are illegal in Canada.",
    "There are more psychoanalysts per capita in Buenos Aires than any other place in the world.",
    "Between 2 and 3 jockeys are killed each year in horse racing.",
    "5,840 people with pillow related injuries checked into U.S. emergency rooms in 1992.",
    "The average woman consumes 6 lbs of lipstick in her lifetime.",
    "Some individuals express concern sharing their soap, rightly so, considering 75% of all people wash from top to bottom.",
    "Conception occurs most in the month of December.",
    "CBS' '60 Minutes' is the only TV show without a theme song/music.",
    "Half of all Americans live within 50 miles of their birthplace.",
    "'Obsession' is the most popular boat name.", "On average, Americans' favorite smell is banana.",
    "If one spells out numbers, they would have to count to One Thousand before coming across the letter 'A'.",
    "Honey is the only food which does not spoil.", "3.9% of all women do not wear underwear.",
    "This common everyday occurrence composed of 59% nitrogen, 21% hydrogen, and 9% dioxide is called a 'fart'.",
    "'Evaluation and Parameterization of Stability and Safety Performance Characteristics of Two and Three Wheeled Vehicular Toys for Riding.' Title of a $230,000 research project proposed by the Department of Health, Education and Welfare, to study the various ways children fall off bicycles.",
    "Babies are born without kneecaps. They don't appear until the child reaches 2-6 years of age.",
    "Meteorologists claim they're right 85% of the time (think about that one!)",
    "In 1980, a Las Vegas hospital suspended workers for betting on when patients would die.",
    "Los Angeles' full name 'El Pueblo de Nuestra Senora la Reina de Los Angeles de Porciuncula' is reduced to 3.63% of its size in the abbreviation 'L.A.'.",
    "If you went out into space, you would explode before you suffocated because there's no air pressure.",
    "The only real person to ever to appear on a pez dispenser was Betsy Ross.",
    "Mike Nesmith's (the guitarist of The Monkeys) mom invented White Out.",
    "Only 6 people in the whole world have died from moshing.",
    "241.     In a test performed by Canadian scientists, using various different styles of music, it was determined that chickens lay the most eggs when pop music was played.",
    "The storage capacity of human brain exceeds 4 Terabytes.",
    "In Vermont, the ratio of cows to people is 10:1",
    "Any free-moving liquid in outer space will form itself into a sphere, because of its surface tension.",
    "The average American looks at eight houses before buying one.",
    "In the average lifetime, a person will walk the equivalent of 5 times around the equator.",
    "Koala is Aboriginal for 'no drink'.", "Shakespeare spelled his OWN name several different ways.",
    "The first contraceptive was crocodile dung used by the ancient Egyptians.",
    "A signature is called a John Hancock because he signed the Declaration of Independence. Only 2 people signed the declaration of independence on July 4. The Last person signed 2 years later.",
    "Arnold Schonberg suffered from triskaidecaphobia, the fear of the number 13.  He died at 13 minutes from midnight on Friday the 13th.",
    "Mozart wrote the nursery rhyme 'twinkle, twinkle, little star' at the age of 5.",
    "Weatherman Willard Scott was the first original Ronald McDonald.",
    "Virginia Woolf wrote all her books standing.",
    "Einstein couldn't speak fluently until after his ninth birthday. His parents thought he was mentally retarded.",
    "Al Capone's business card said he was a used furniture dealer.",
    "Deborah Winger did the voice of E.T.",
    "Kelsey Grammar sings and plays the piano for the theme song of Fraiser.",
    "Thomas Edison, acclaimed inventor of the light bulb, was afraid of the dark.",
    "In England, the Speaker of the House is not allowed to speak.",
    "You can sail all the way around the world at latitude 60 degrees south.",
    "The earth weighs around 6,588,000,000,000,000,000,000,000,000 tons.",
    "Peanuts are one of the ingredients of dynamite.", "Porcupines can float in water.",
    "The average person's left hand does 56% of the typing.",
    "A shark is the only fish that can blink with both eyes.",
    "The longest one-syllable word in the English language is 'screeched.'",
    "All of the clocks in the movie 'Pulp Fiction' are stuck on 4:20, a national pot-smokers hour.",
    "'Dreamt' is the only English word that ends in the letters 'mt.'",
    "Almonds are a member of the peach family.",
    "Winston Churchill was born in a ladies' room during a dance.",
    "Maine is the only state whose name is just one syllable.",
    "There are only four words in the English language which end in 'dous': tremendous, horrendous, stupendous, and  hazardous.",
    "Tigers not only have striped fur, they have striped skin!",
    "In most advertisements, including newspapers, the time displayed on a watch is 10:10.",
    "On the ground, a group of geese is a gaggle, in the sky it is a skein.",
    "To Ensure Promptness, one is expected to pay beyond the value of service – hence the later abbreviation: T.I.P.",
    "When the University of Nebraska Cornhuskers play football at home, the stadium becomes the state's third largest city.",
    "The characters Bert and Ernie on Sesame Street were named after Bert the cop and Ernie the taxi driver in Frank Capra's 'Its A Wonderful Life.'",
    "A dragonfly has a lifespan of 24 hours.", "A dime has 118 ridges around the edge.",
    "On an American one-dollar bill, there is an owl in the upper left-hand corner of the '1'encased in the 'shield' and a spider hidden in the front upper right-hand corner.",
    "The name for Oz in the 'Wizard of Oz' was thought up when the creator, Frank Baum, looked at his filing cabinet and saw A-N, and O-Z; hence the name 'OZ.'",
    "The microwave was invented after a researcher walked by a radar tube and a chocolate bar melted in his pocket.",
    "Mr. Rogers is an ordained minister.", "John Lennon's first girlfriend was named Thelma Pickles.",
    "There are 336 dimples on a regulation golf ball.",
    "The scene where Indiana Jones shoots the swordsman in Raider’s of the Lost Ark was Harrison Ford's idea so that he could take a bathroom break.",
    "A crocodile cannot stick its tongue out.", "A snail can sleep for three years.",
    "All polar bears are left-handed.", "China has more English speakers than the United States.",
    "Elephants are the only animals that can't jump.",
    "February 1865 is the only month in recorded history not to have a full moon.",
    "If the population of China walked past you in single file, the line would never end because of the rate of reproduction.",
    "If you yelled for 8 years, 7 months and 6 days, you will have produced enough sound energy to heat one cup of coffee.",
    "In the last 4000 years, no new animals have been domesticated.",
    "Leonardo Da Vinci invented the scissors.",
    "The word 'set' has more definitions than any other word in the English language.",
    "Nutmeg is extremely poisonous if injected intravenously.",
    "On average, people fear spiders more than they do death.",
    "One of the reasons marijuana is illegal today is because cotton growers in the 1930s lobbied against hemp farmers they saw it as competition.",
    "Shakespeare invented the word 'assassination' and 'bump'.", "Some lions mate over 50 times a day.",
    "Starfish haven't got brains.", "The ant always falls over on its right side when intoxicated.",
    "The name of all continents in the world end with the same letter that they start with.",
    "There are two credit cards for every person in the United States.",
    "The longest word comprised of one row on the keyboard is: TYPEWRITER",
    "You can't kill yourself by holding your breath. ",
    "The average person spends 12 weeks a year 'looking for things'.",
    "The symbol on the 'pound' key (#) is called an octothorpe.. ",
    "The dot over the letter 'i' is called a tittle. ", "Ingrown toenails are hereditary. ",
    "'Underground' is the only word in the English language that begins and ends with the letters 'und'",
    "The longest word in the English language, according to the Oxford English Dictionary, is: pneumonoultramicroscopicsilicovolcanoconiosis.. ",
    "The longest place-name still in use is: Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokaiakitnatahu, a New Zealand hill. ",
    "An ostrich's eye is bigger than its brain. ",
    "Alfred Hitchcock didn't have a belly button. It was eliminated when he was sewn up after surgery.",
    "Telly Savalas and Louis Armstrong died on their birthdays. ",
    "Donald Duck's middle name is Fauntleroy. ",
    "The muzzle of a lion is like a fingerprint - no two lions have the same pattern of whiskers. ",
    "Steely Dan got their name from a sexual device depicted in the book 'The Naked Lunch'. ",
    "The Ramses brand condom is named after the great pharoh Ramses II who fathered over 160 children.",
    "There is a seven letter word in the English language that contains ten words without rearranging any of its letters, 'therein': the, there, he, in, rein, her, here, ere, therein, herein. ",
    "A goldfish has a memory span of three seconds. ",
    "Cranberries are sorted for ripeness by bouncing them; a fully ripened cranberry can be dribbled like a basketball. ",
    "The male gypsy moth can 'smell' the virgin female gypsy moth from 1.8 miles away. ",
    "The letters KGB stand for Komitet Gosudarstvennoy Bezopasnosti. ",
    "The word 'dexter' whose meaning refers to the right hand is typed with only the left hand. ",
    "To 'testify' was based on men in the Roman court swearing to a statement made by swearing on their testicles. ",
    "Facetious and abstemious contain all the vowels in the correct order, as does arsenious, meaning 'containing arsenic.' ",
    "The word 'Checkmate' in chess comes from the Persian phrase 'Shah Mat,' which means 'the king is dead.'",
    "The first episode of 'Joanie Loves Chachi' was the highest rated American program in the history of Korean television, a country where 'Chachi' translates to 'penis'. ",
    "Rubber bands last longer when refrigerated. ",
    "The national anthem of Greece has 158 verses. No one in Greece has memorized all 158 verses. ",
    "Two-thirds of the world's eggplant is grown in New Jersey. ",
    "The giant squid has the largest eyes in the world.", "Giraffes have no vocal cords.",
    "The pupils of a goat's eyes are square.", "Van Gogh only sold one painting when he was alive.",
    "A standard slinky measures 87 feet when stretched out.",
    "The highest per capita Jell-O comsumption in the US is Des Moines.",
    "If a rooster can't fully extend its neck, it can't crow.",
    "There were always 56 curls in Shirley Temple's hair.",
    "The eyes of a donkey are positioned so that it can see all four feet at all times.",
    "Worcestershire sauce in essentially an Anchovy Ketchup.",
    "Rhode Island is the only state which the hammer throw is a legal high school sport.",
    "The average lifespan of an eyelash is five months.", "A spider has transparent blood.",
    "Every acre of American crops harvested contains 100 pounds of insects.",
    "Prince Charles is an avid collecter of toilet seats.",
    "The most common street name in the U.S. is Second Street.",
    "Tehran is the most expensive city on earth.",
    "The sweat drops drawn in cartoon comic strips are called pleuts.",
    "Babies are most likely to be born on Tuesdays.",
    "The HyperMart outside of Garland Texas has 58 check-outs.",
    "The Minneapolis phone book has 21 pages of Andersons.",
    "In the 1980's American migraines increased by 60%.",
    "Poland is the 'stolen car capital of the world'.",
    "Jefferson invented the dumbwaiter, the monetary system, and the folding attic ladder.",
    "The S in Harry S. Truman did not stand for anything.", "In Miconesia, coins are 12 feet across.",
    "A horse can look forward with one eye and back with the other.",
    "Shakespeare is quoted 33,150 times in the Oxford English dictionary.",
    "The word Pennsylvania is misspelled on the Liberty Bell.",
    "NBA superstar Michael Jordan was originally cut from his high school basketball team.",
    "You spend 7 years of your life in the bathroom.",
    "A family of 26 could go to the movies in Mexico city for the price of one in Tokyo.",
    "10,000 Dutch cows pass through the Amsterdam airport each year.",
    "Approximately every seven minutes of every day, someone in an aerobics class pulls their hamstring.",
    "Simplistic passwords contribute to over 80% of all computer password break-ins.",
    "The top 3 health-related searches on the Internet are (in this order): Depression, Allergies, & Cancer.",
    "Dentists have recommended that a toothbrush be kept at least 6 feet away from a toilet to avoid airborne particles resulting from the flush.",
    "Most dust particles in your house are made from dead skin.",
    "Venus is the only planet that rotates clockwise.",
    "Oak trees do not produce acorns until they are fifty years of age or older.",
    "The first owner of the Marlboro company died of lung cancer.",
    "All US Presidents have worn glasses; some just didn't like being seen wearing them in public.",
    "Mosquito repellents don't repel. They hide you. The spray blocks the mosquito's sensors so they don't know you're there.",
    "Walt Disney was afraid of mice.",
    "The site with the highest number of women visitors between the age of 35 and 44 years old: Alka-Seltzer.com",
    "The king of hearts is the only king without a mustache.", "Pearls melt in vinegar.",
    "It takes 3,000 cows to supply the NFL with enough leather for a year's supply of footballs.",
    "Thirty-five percent of people who use personal ads for dating are already married.",
    "The 3 most valuable brand names on earth are Marlboro, Coca-Cola, and Budweiser (in that order).",
    "Humans are the only primates that don't have pigment in the palms of their hands.",
    "Months that begin on a Sunday will always have a 'Friday the 13th'.",
    "The fingerprints of koala bears are virtually indistinguishable from those of humans, so much so that they can be easily confused at a crime scene.",
    "The mask worn by Michael Myers in the original 'Halloween' was actually a Captain Kirk mask painted white.",
    "The only two days of the year in which there are no professional sports games--MLB, NBA, NHL, or NFL--are the day before and the day after the Major League All-Star Game.",
    "Only one person in two billion will live to be 116 or older.",
    "When the French Academy was preparing its first dictionary, it defined 'crab' as, 'A small red fish, which walks backwards.' This definition was sent with a number of others to the naturalist Cuvier for his approval.  The scientist wrote back, 'Your definition, gentlemen, would be perfect, only for three exceptions. The crab is not a fish, it is not red and it does not walk backwards.'",
    "Dr. Jack Kevorkian first patient has Alzheimer's disease.",
    "Fictional/horror writer Stephen King sleeps with a nearby light on to calm his fear of the dark.",
    "It's possible to lead a cow upstairs but not downstairs.",
    "It was discovered on a space mission that a frog can throw up. The frog throws up its stomach first, so the stomach is dangling out of its mouth. Then the frog uses its forearms to dig out all of the stomach's contents and then swallows the stomach back down.",
    "The very first song played on MTV was 'Video Killed The Radio Star' by the Buggles.",
    "William Marston engineered one of the earliest forms of the polygraph in the early 1900's. Later he went on to create the comic strip Wonder Woman, a story about a displaced Amazon princess who forces anyone caught in her magic lasso to tell the truth",
    "Americans travel 1,144,721,000 miles by air every day",
    "The the U.S. you dial '911'. In Stockholm, Sweden you dial 90000",
    "38% of American men say they love their cars more than women",
    "The U.S. military operates 234 golf courses", "100% of lottery winners do gain weight",
    "Bullet proof vests, fire escapes, windshield wipers, and laser printers were all invented by women",
    "A cat has 32 muscles in each ear.", "A duck's quack doesn't echo, and no one knows why.",
    "Cats urine glows under a black light.", "In every episode of Seinfeld there is a Superman somewhere.",
    "Lorne Greene had one of his nipples bitten off by an alligator while he was host of 'Lorne Greene's Wild Kingdom.'",
    "Pamela Anderson Lee is Canada's Centennial Baby, being the first baby born on the centennial anniversary of Canada's independence.",
    "Pinocchio is Italian for 'pine head.'",
    "When possums are playing 'possum', they are not 'playing.' They actually pass out from sheer terror.",
    "Who's that playing the piano on the 'Mad About You' theme? Paul Reiser himself.",
    "Winston Churchill was born in a ladies' room during a dance.", "Most lipstick contains fish scales!",
    "Donald Duck comics were banned from Finland because he doesn't wear pants!",
    "There are more than 10 million bricks in the Empire State Building!",
    "Camels have three eyelids to protect themselves from blowing sand!",
    "The placement of a donkey's eyes in its' heads enables it to see all four feet at all times!",
    "The average American/Canadian will eat about 11.9 pounds of cereal per year!",
    "Over 1000 birds a year die from smashing into windows!",
    "The state of Florida is bigger than England!", "Dolphins sleep with one eye open!",
    "In the White House, there are 13,092 knives, forks and spoons!",
    "Recycling one glass jar, saves enough energy to watch T.V for 3 hours!",
    "Owls are one of the only birds who can see the color blue!",
    "Honeybees have a type of hair on their eyes!", "A jellyfish is 95 percent water!",
    "In Bangladesh, kids as young as 15 can be jailed for cheating on their finals!",
    "The katydid bug hears through holes in its hind legs!",
    "Q is the only letter in the alphabet that does not appear in the name of any of the United States!",
    "166,875,000,000 pieces of mail are delivered each year in the US",
    "Bats always turn left when exiting a cave",
    "The praying mantis is the only insect that can turn its head", "Daffy Duck's middle name is 'Dumas'",
    "In Disney's Fantasia, the Sorcerer's name is 'Yensid' (Disney backwards.)",
    "In The Empire Strikes Back there is a potato hidden in the asteroid field",
    "Walt Disney holds the world record for the most Academy Awards won by one person, he has won twenty statuettes, and twelve other plaques and certificates",
    "James Bond's car had three different license plates in Goldfinger",
    "Canada makes up 6.67 percent of the Earth's land area",
    "South Dakota is the only U.S state which shares no letters with the name of it's capital",
    "The KGB is headquartered at No. 2 Felix Dzerzhinsky Square, Moscow",
    "The Vatican city registered 0 births in 1983", "Spain leads the world in cork production",
    "There are 1,792 steps in the Eiffel Tower",
    "There are 269 steps to the top of the Leaning Tower of Pisa",
    "Leonardo da Vinci could write with one hand while drawing with the other",
    "Rubber bands last longer when refrigerated.", "Peanuts are one of the ingredients of dynamite.",
    "The national anthem of Greece has 158 verses. No one in Greece has memorized all 158 verses.",
    "There are 293 ways to make change for a dollar.",
    "The average secretary’s left hand does 56% of the typing.",
    "A shark is the only fish that can blink with both eyes.",
    "There are more chickens than people in the world (at least before that chicken-flu thing).",
    "Two-thirds of the world’s eggplant is grown in New Jersey.",
    "The longest one-syllable word in the English language is 'screeched.'",
    "All of the clocks in the movie Pulp Fiction are stuck on 4:20.",
    "No word in the English language rhymes with month, orange, silver or purple.",
    "'Dreamt' is the only English word that ends in the letters 'mt'.",
    "All 50 states are listed across the top of the Lincoln Memorial on the back of the $5 bill.",
    "Almonds are members of the peach family.",
    "Winston Churchill was born in a ladies’ room during a dance.",
    "Maine is the only state whose name is just one syllable.",
    "There are only four words in the English language which end in 'dous': tremendous, horrendous, stupendous, and hazardous.",
    "Los Angeles’s full name is 'El Pueblo de Nuestra Senora la Reina de los Angeles de Porciuncula'. And can be abbreviated to 3.63% of its size, 'L.A.'",
    "A cat has 32 muscles in each ear.", "An ostrich’s eye is bigger than it’s brain.",
    "Tigers have striped skin, not just striped fur.",
    "In most advertisements, including newspapers, the time displayed on a watch is 10:10.",
    "Al Capone’s business card said he was a used furniture dealer.",
    "The only real person to be a Pez head was Betsy Ross.",
    "When the University of Nebraska Cornhuskers plays football at home, the stadium becomes the state’s third largest city.",
    "The characters Bert and Ernie on Sesame Street were named after Bert the cop and Ernie the taxi driver in Frank Capra’s 'Its A Wonderful Life'",
    "A dragonfly has a lifespan of 24 hours.", "A goldfish has a memory span of three seconds.",
    "A goldfish has a memory span of three seconds.", "A dime has 118 ridges around the edge.",
    "On an American one-dollar bill, there is an owl in the upper left-hand corner of the '1' encased in the 'shield' and a spider hidden in the front upper right-hand corner.",
    "It’s impossible to sneeze with your eyes open.", "The giant squid has the largest eyes in the world.",
    "Who’s that playing the piano on the 'Mad About You' theme? Paul Reiser himself.",
    "The male gypsy moth can 'smell' the virgin female gypsy moth from 1.8 miles away (pretty good trick).",
    "In England, the Speaker of the House is not allowed to speak.",
    "The name for Oz in the 'Wizard of Oz' was thought up when the creator, Frank Baum, looked at his filing cabinet and saw A-N, and O-Z, hence 'Oz.'",
    "The microwave was invented after a researcher walked by a radar tube and a chocolate bar melted in his pocket.",
    "Mr. Rogers is an ordained minister.", "John Lennon’s first girlfriend was named Thelma Pickles.",
    "The average person falls asleep in seven minutes.",
    "There are 336 dimples on a regulation golf ball.",
    "'Stewardesses' is the longest word that is typed with only the left hand.",
    "The 'pound' key on your keyboard (#) is called an octotroph.",
    "The only domestic animal not mentioned in the Bible is the cat.",
    "The 'dot' over the letter 'i' is called a tittle.",
    "Table tennis balls have been known to travel off the paddle at speeds up to 160 km/hr.",
    "Pepsi originally contained pepsin, thus the name.",
    "The original story from 'Tales of 1001 Arabian Nights' begins, 'Aladdin was a little Chinese boy.'",
    "Nutmeg is extremely poisonous if injected intravenously.",
    "Honey is the only natural food that is made without destroying any kind of life. What about milk you say? A cow has to eat grass to produce milk and grass are living.",
    "Hawaiian alphabet only has 12 letters: A, E, I, O, U, H, K, L, M, N, P, W",
    "Honey is the only food that does not spoil.",
    "And one single teaspoon of honey represents the life work of 12 bees.",
    "Flamingos only can eat with their heads upside down.",
    "Lighter was invented ten years before the match was.",
    "It’s physically impossible for a pig to look up at the sky.",
    "The first internet domain name to ever be registered is Symbolics.com on March 15th, 1985.",
    "Humans are born with 350 bones in their body, but when reaching adulthood, we only 260.",
    "There are 150 verses in Greek national anthem which making it the longest national anthem in the world.",
    "This is impossible to tickle yourself.", "A typical pencil can draw a line that is 35 miles long.",
    "Astronauts get taller in space due to the lack of gravity.",
    "The total surface area of human lungs is 750 square feet. That’s roughly the same area as on-side of a tennis court.",
    "Mosquitos have contributed to more deaths than any animals on earth.",
    "An octopus has 3 hearts, 9 brains & blue blood.",
    "The hair on a polar bear is actually not white but clear. They appear white because it reflects light.",
    "A chameleon can move its eyes in two different directions at the same time.",
    "Buttermilk does not contain any butter and actually low in fat.",
    "A giraffe can go longer without water than a camel can.",
    "Australia has the biggest camel population in the world.", "Snails can sleep up to 3 years.",
    "Methane gases produced by cow products as much pollution as cars do.",
    "The majority of the duct in your house is made up from your own dead skin.",
    "Most lipstick contains fish scales.", "Most ice-cream contains pig skins (Gelatin).",
    "The Philippine island of Luzon contains a lake that contains an island that contains a lake that contains another island.",
    "Hudson Bay Area in Canada had less gravity than rest of the world and scientists do not know why.",
    "Only one to two percent of the entire world population are natural redheads.",
    "Sloppy handwriting has doctors kills more than 7,000 people and injures more than 1.5million people annually due to getting the wrong medication.",
    "Putting sugar on a wound or cut will greatly reduce pain and shorten healing process.",
    "Real diamonds do not show up in X-ray.",
    "Due to extreme pressure and weather conditions, it literally rains diamonds on Neptune and Uranus.",
    "There are 7 different kinds of twins: Identical, Fraternal, Half-Identical, Mirror Image Twins, Mixed Chromosome Twins, Superfecundation and Superfetation.",
    "Before the 17th century, carrots were actually purple. They didn’t get their orange color until mutation occupied.",
    "If the sun is scaled down to the size of a white blood cell, the Milky Way would be equal the size of the United States.",
    "A grammatical pedantry syndrome is a form of OCD in which suffers feel the need to correct every grammatical error that they see.",
    "Scorpions can hold their breath underwater for up to 6 days.",
    "In zero gravity, a candle’s flame is round and blue.",
    "Only 8 percent of the world’s money exists in physical form, the rest is in computers.",
    "Crows are able to recognize human faces and even hold grudges against ones that they don’t like.",
    "Your cellphone carries up to ten times more bacteria than a toilet seat.",
    "Humans and bananas share about 50 percent of the same DNA.",
    "Humans have fewer chromosomes than a potato.",
    "An American Pharmacist named John Pemberton invented Coca-Cola who advertises it as a nerve tonic for curing headaches and fatigue.",
    "Statistically, you are more likely to die on the way to buy a lottery ticket than you are to win the lottery itself.",
    "The word checkmate comes from the Arabic which means 'the king is dead.'",
    "Hot water turns to ice faster than cool water. This is known as the Mpemba effect.",
    "Apollo 7 Mission was the first 'astronaut ice cream' flew in space. However, it was so unpopular among astronauts and was retired from the menu after only one trip into space.",
    "Apollo 8 astronauts were the first to celebrate Christmas in space.",
    "IV Is The Roman Numeral designation for 4 everywhere. However, on the clock face, 4 is displayed as 'IIII'.",
    "The Apple Macintosh had the signatures Of its design team engraved inside its case.",
    "Japan has the most vending machines per capita, a staggering 1:23.",
    "A study by University Chicago in 1915, it concluded that the easiest color to spot at a distance is the color yellow. Which is why the most popular color for taxi cabs are yellow.",
    "Japanese police declare murders that they cannot solve as suicides, in order to save faces and keep crime rate artificially low.",
    "The smallest poisonous frogs only 10 millimeters (0.393701 inch) in length.",
    "Farting helps to reduce blood pressure and is good for your overall health.",
    "In 1994, the US Air Force did research on creating a gay bomb (are informal names for theoretical non-lethal chemical weapon) which is a non-lethal bomb containing very strong human sexual pheromones that would make the enemy forces attracted to each other.",
    "There are around 1,584 people in the United States named 'Seven'.",
    "The classic heart shape that we all know was meant to be two hearts fused together.",
    "The water we drink is older than the sun. The sun is 4.6 billion years old.",
    "The water on our planet is very old. The water we have now is the same water that existed hundreds of millions of year ago. The next time you drink a glass of water, you could be about to sip on dinosaur pee.",
    "Meanwhile, about 40% of Americans think humans and dinosaurs existed at the same time.",
    "Nobody knows who named our planet 'Earth'.",
    "Michael Nicholson from Michigan. He has one bachelor’s degree, two associate’s degrees, 22 master’s degrees, three specialist degrees and one doctoral degree, making him the most credentialed person in history.",
    "Practicing a kill in your head will make you better at it, but only if you’re already good at it.",
    "If two identical twins have children with another pair of identical twins, then their children will genetically be full siblings.",
    "In Biertan village (located in Transylvania, Romania) the church had a 'divorce-reconciliation room.' Couples that wanted to get a divorce had to live in a room for two weeks with one small bed, one chair, one table, one plate and one spoon. In 300 years, they only had one divorce.",
    "Killing a panda in China is a seriously crime. It is punishable by death.",
    "December 4th is the National Cookie Day!",
    "Beards can slow the aging process by stopping water from leaving the skin, keeping it moisturized.",
    "A survey found that 33% of men and 43% of women claimed that they had fallen in love with someone they did not initially find attractive.",
    "Most people dream in color, but those who grow up watching television in black and white are more likely to dream in black and white.",
    "Mixing your drinks with diet soda can get you drunk about 18% faster than regular soda. Hummm…",
    "The number of H2O molecules in 10 drops of water is roughly equal to the total amount of stars in the universe.",
    "Octopuses have copper-based blood instead of iron-based blood, which is why their blood is blue rather than red.",
    "Also, they have three hearts and nine brains",
    "The hormones responsible for your growth are only produced when you sleep.",
    "You touch your face an average of once every three minutes. And you properly touched your face after you read it.",
    "People who sleep less than six hours a night are 4.2 times more likely to catch a cold compared those who get more than seven hours of sleep.",
    "Dogs can make about 100 different facial expressions.",
    "Iceland has no army as is often recognized as the most peaceful country in the world.",
    "Shigeru Miyamoto – maker of Super Mario Bros. and Donkey Kong – is not allowed to bike to work because his safety is too important to Nintendo.",
    "Every year, women lose approximately 1.73 billion bobby pins.",
    "Dolphins give each other 'names' – Specific sounds that they use to call friends and family.",
    "Chimpanzee babies like to play with dolls – They’ll make dolls out of sticks and rocks for themselves.",
    "Squirrels plant thousands of trees every year, simply by forgetting where they put their acorns.",
    "Koalas can sleep for up to 20 hours a day.",
    "The average woman will spend one full year of her life trying to decide what to wear.",
    "The average woman owns eight times more makeup than she actually uses.",
    "Rainbows that appear at night are called 'moonbows.'",
    "100 million years ago, crocodiles had long legs and could gallop after their prey.",
    "The real Top Gun school give a $5 fine to any staff member that quotes the movie.")

@tasks.loop(minutes=1)
async def fotd_check():
    last = bot.refr.setdefault("fotd", 0)
    print('fotd-last', last)
    print('diff', time.time() - last)
    if time.time() - last >= 86400:
        index = bot.refr.setdefault("factindex", -1)
        index += 1
        print('fotd-index', index)
        fotd = bot.get_channel(813535171117580350)
        role = bot.get_guild(719946380285837322).get_role(813704961103888434)
        upv = await fotd.send(f"__**{role.mention} #{index+100}**__\n\n"
                        f"{facts[index]}")
        try:
            await upv.add_reaction("<:Upvote:837564803090219028>")
        except:
            pass
        
        bot.refr["factindex"] = index
        bot.refr["fotd"] = time.time()

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
    if data == "error":
        return "error"
    if len(data["active"]) == len(actlist):
        count = 0
        for i in data["active"]:
            i.set_footer(text=f"Bot by {bot.dev} | Last Refreshed", icon_url=sampfp)
            i.timestamp = datetime.datetime.utcnow()
            await actlist[count].edit(embed=i)
    else:
        return await view(channel, clan=clan, via="sam123")

    if len(data["expired"]) == len(actlist):
        for i in data["expired"]:
            count = 0
            i.set_footer(text=f"Bot by {bot.dev} | Last Refreshed", icon_url=sampfp)
            i.timestamp = datetime.datetime.utcnow()
            await explist[count].edit(embed=i)
    else:
        return await view(channel, clan=clan, via="sam123")

async def update_links():
    with open("links.json", "w") as f:
        f.write(str(json.dumps(bot.links, indent=2)))
    await bot.get_channel(854721559359913994).send(file=discord.File("links.json"))

async def get_admin():
    return bot.refr["719946380285837322"]

async def spam_protect(userid):
    if userid in bot.refr["disregarded"]:
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

async def linklog(ign, user, t, linkedby=None):
    if t == "l":
        embed = discord.Embed(description=f"`{user}` got linked with `{ign}`", colour=success_embed)
        if linkedby is not None: embed.set_footer(text=f"Force-Linked By: {linkedby}")
    else:
        embed = discord.Embed(description=f"`{user}` got unlinked with `{ign}`", colour=error_embed)
    embed.footer.timestamp = datetime.datetime.utcnow()
    await bot.linkinglogs.send(embed=embed)

async def timeout(user):
    bot.interlist.append(user.id)
    await asyncio.sleep(3600)
    bot.interlist.remove(user.id)

async def conv_rem(msg):
    days = 0
    hrs = 0
    mins = 0
    secs = 0
    try:
        if "d" in msg:
            newmsg = msg.split("d")
            days = int(newmsg[0])
            newmsg.pop(0)
            msg = "".join(newmsg)
        if "h" in msg:
            newmsg = msg.split("h")
            hrs = int(newmsg[0])
            newmsg.pop(0)
            msg = "".join(newmsg)
        if "m" in msg:
            newmsg = msg.split("m")
            mins = int(newmsg[0])
            newmsg.pop(0)
            msg = "".join(newmsg)
        if "s" in msg:
            newmsg = msg.split("s")
            secs = int(newmsg[0])
            newmsg.pop(0)
            msg = "".join(newmsg)
        return (days*86400) + (hrs*3600) + (mins*60) + secs
    except:
        return "error"

@tasks.loop(seconds=2)
async def handle_rems():
    rems = bot.refr["rems"]
    for i, aut in rems.items():
        for j in aut:
            tleft = int(j["time"] - time.time() + j["tadd"])
            if tleft <= 0:
                aut.remove(j)
                await exec_rem(j, i)
        rems[i] = aut
    bot.refr["rems"] = rems

async def exec_rem(rem, userid):
    user = bot.get_user(int(userid))
    if user is None: return
    embed = discord.Embed(title="Reminder",
                          description=f"{rem['desc']}\n"
                                      f"Set at: <t:{int(rem['tadd'])}:F> (<t:{int(rem['tadd'])}:R>)",
                          color=embedcolor)
    embed.set_author(name=user.name, icon_url=user.default_avatar.url)
    embed.set_thumbnail(
        url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
    try: await user.send(embed=embed)
    except: await bot.get_channel(rem["chl"]).send(f"{user.mention}", embed=embed)
    await close_admin()

@bot.command()
@commands.check(general)
async def view(ctx, clan=None, via=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if bot.cwpause:
        embed = discord.Embed(title="Wars Break",
                              description="Clan wars are not currently running. Please use this command after wars start!",
                              colour=error_embed)
        embed.set_footer(text="To view past contracts and analytics, use 'v.cw'")
        return await ctx.reply(embed=embed)
    ctx2 = ctx
    if via == "sam123" and clan is not None:
        pass
    else:
        if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
            return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
        if clan is not None:
            if ctx.author.id not in staff:
                clan = "VNTA"
            else:
                if ctx.channel.id not in staffchl:
                    return await ctx.reply(f"For security reasons, this command cannot be used in a public channel.\n"
                                           f"Please go to {' or '.join([x.mention for x in [bot.get_channel(y) for y in staffchl]])}.")
        else:
            clan = "VNTA"
        if ctx.channel.id not in staffchl+[813437673926557736]:
            return await ctx.reply(
                "You are not allowed to use this command in public channel")
        await ctx.message.add_reaction(loading)
        ctx = ctx.channel
    data = await embed_view(clan)
    if data == "error":
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        await ctx2.message.clear_reaction(loading)
        return await ctx.send(embed=embed)
    maybeupdate = {}
    for i in data.keys():
        em = data[i]
        ids = []
        for j in em:
            a = await ctx.send(embed=j)
            ids.append(a.id)
            #await ctx2.message.clear_reaction(loading)
        if via == "sam123" and clan is not None:
            maybeupdate[i] = ids
    if len(maybeupdate.values()) != 0:
        maybeupdate["chl"] = ctx.id
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
        await view(ctx.channel, clan=clan, via="sam123")
        await close_admin()

@bot.command()
@commands.check(general)
async def end(ctx=None, clan=None, via=False):
    if not via:
        if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
        if bot.cwpause:
            embed = discord.Embed(title="Wars Break",
                                  description="Clan wars are not currently running. Please use this command after wars start!",
                                  colour=error_embed)
            embed.set_footer(text="To view past contracts and analytics, use 'v.cw'")
            return await ctx.reply(embed=embed)
        if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
            return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
        if clan is not None:
            if ctx.author.id not in staff:
                print("not qualified")
                clan = "VNTA"
            else:
                if ctx.channel.id not in staffchl:
                    return await ctx.reply(f"For security reasons, this command cannot be used in a public channel.\n"
                                           f"Please go to {' or '.join([x.mention for x in [bot.get_channel(y) for y in staffchl]])}.")
        else:
            clan = "VNTA"
        if ctx.channel.id not in staffchl+[813437673926557736]:
            return await ctx.reply("You are not allowed to use this command in public chat")
        await ctx.message.add_reaction(loading)
    print("reqesting for", clan)
    data = await getdata(clan)
    print(data)
    if data == "error":
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        await ctx.message.clear_reaction(loading)
        return await ctx.send(embed=embed)
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
            active_con = discord.Embed(description=f"```css\n{active.get_string()[count:count+2000]}```",
                                       color=color)
            count += 2000
            actlist.append(active_con)

    for j in actlist:
        j.set_footer(text=f"Est. Kills: {finalkills} | Bot by {bot.dev}", icon_url=sampfp)
        if not via: a = await ctx.send(embed=j)
    if not via:
        return await ctx.message.clear_reaction(loading)
    newdata = []
    for i in data:
        dat = {}
        for k, v in i.items():
            if k in ["username", "contract"]:
                dat[k] = v
        newdata.append(dat)
    return int(finalkills), newdata

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

@bot.command()
@commands.check(general)
async def link(ctx, *, ign):
    d = bot.links.get(str(ctx.author.id), [])
    if ign.lower() in [x.lower for x in d]:
        return await ctx.send("You already have this account linked")
    await ctx.message.add_reaction(loading)
    if ign.lower() in bot.cache:
        t = bot.cache[ign.lower()]["time"]
        if time.time() - t < 15:
            userdata = bot.cache[ign.lower()]["data"]
        else:
            async with aiohttp.ClientSession() as session:
               async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
                    if data.status != 200:
                        embed = discord.Embed(title=f"{economyerror} Error",
                                              description="API didnt respond in time",
                                              color=error_embed)
                        embed.set_footer(text="Please try again later")
                        await ctx.message.clear_reaction(loading)
                        return await ctx.send(embed=embed)
                    userdata = json.loads(await data.text())
                    if not userdata["success"]:
                        await ctx.message.clear_reaction(loading)
                        return await ctx.reply(userdata["error"])
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
                if data.status != 200:
                    embed = discord.Embed(title=f"{economyerror} Error",
                                          description="API didnt respond in time",
                                          color=error_embed)
                    await ctx.message.clear_reaction(loading)
                    embed.set_footer(text="Please try again later")
                    return await ctx.send(embed=embed)
                userdata = json.loads(await data.text())
                if not userdata["success"]:
                    await ctx.message.clear_reaction(loading)
                    return await ctx.reply(userdata["error"])
    randflag = random.choice(flags_list)
    newflag = randflag[2]
    embed = discord.Embed(title="Link your account..",
                          description="```diff\n"
                                      f"- Open krunker.io and login with your account\n"
                                      f"+ Click your profile on top right and go to settings\n"
                                      f"- Change your flag to '{randflag[0]}'\n"
                                      f"+ Enter the match and finish it.```",
                          color=embedcolor)
    embed.set_footer(text="Once done, react below..")
    await ctx.message.clear_reaction(loading)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(economysuccess)
    await msg.add_reaction(economyerror)
    bot.pendings[msg.id] = (ctx.author.id, str(ign), newflag)

@bot.command(aliases=["fl", "forcel", "flink"])
@commands.check(general)
async def forcelink(ctx, user:discord.Member, *, ign):
    if ctx.author.id not in staff: return

    t = bot.links.get(str(user.id), {"main": ign, "all": []})
    t["all"] = list(set(t["all"]))
    if ign.lower() in [x.lower() for x in t["all"]]:
        return await ctx.reply(f"User is already linked with `{ign}`")
    t["all"].append(ign)
    bot.links[str(user.id)] = t
    await update_links()
    await user.send(f"✅ You were force-linked with `{ign}`.\n"
                    f"If this seems incorrect, you can unlink using `v.unlink {ign}` and report the issue to {bot.dev.mention}")
    await ctx.reply("Done")
    await linklog(ign=ign, user=user, t="l", linkedby=ctx.author)

@bot.command()
@commands.check(general)
async def unlink(ctx, *, ign):
    t = bot.links.get(str(ctx.author.id), {"main": ign, "all": []})
    t["all"] = list(set(t["all"]))
    found = False
    totalunlink = False
    for i in t["all"]:
        if i.lower() == ign.lower():
            t["all"].remove(i)
            if t["main"].lower() == ign.lower():
                if len(t["all"]) != 0:
                    t["main"] = t["all"][0]
                else:
                    totalunlink = True
            found = True
            break
    if not found: return await ctx.reply("You can only unlink the accounts which are linked to you")
    if totalunlink: bot.links.pop(str(ctx.author.id))
    else: bot.links[str(ctx.author.id)] = t
    await update_links()
    await ctx.send(f"✅ You are unlinked with `{ign}`")
    await linklog(ign=ign, user=ctx.author, t="ul")

@bot.command(aliases=["con"])
@commands.check(general)
async def contract(ctx, *, ign=None):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if bot.cwpause:
        embed = discord.Embed(title="Wars Break",
                              description="Clan wars are not currently running. Please use this command after wars start!",
                              colour=error_embed)
        embed.set_footer(text="To view past contracts and analytics, use 'v.cw'")
        return await ctx.reply(embed=embed)
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA clan members are given the exclusive rights to use the bot.")
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
                return await ctx.reply(embed=embed)
            ign = ign["main"]
    await ctx.message.add_reaction(loading)
    personclan = await checkuserclan(ign)
    if personclan == "no":
        return await ctx.send(embed=discord.Embed(description=f"{economyerror} User not in any clan"))
    data = await getdata(personclan)
    if data == "error":
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        await ctx.message.clear_reaction(loading)
        return await ctx.send(embed=embed)
    data = data["data"]["members"]
    found = False
    for i in data:
        if ign.lower() == i["username"].lower():
            userdata = i
            con = i["contract"]
            found = True
            break
    if not found:
        return await ctx.reply("Something went wrong.. Maybe try again")
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
        if timeplayed >= 10800:
            est = "-"
            kpg = con["kills"] / 45
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
    await ctx.message.clear_reaction(loading)
    await ctx.send(embed=embed, file=discord.File(imagebytes, filename="contract.png"))

@bot.command(aliases=["p", "pf"])
@commands.check(general)
async def profile(ctx, *, ign=None, via=False):
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if not via:
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
    await ctx.message.add_reaction(loading)
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
    if ign.lower() in bot.cache:
        t = bot.cache[ign.lower()]["time"]
        if time.time() - t < 15:
            userdata = bot.cache[ign.lower()]["data"]
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
                    if data.status != 200:
                        embed = discord.Embed(title=f"{economyerror} Error",
                                              description="API didnt respond in time",
                                              color=error_embed)
                        embed.set_footer(text="Please try again later")
                        return await ctx.send(embed=embed)
                    userdata = json.loads(await data.text())
                    if not userdata["success"]:
                        return await ctx.reply(userdata["error"])
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
                if data.status != 200:
                    embed = discord.Embed(title=f"{economyerror} Error",
                                          description="API didnt respond in time",
                                          color=error_embed)
                    embed.set_footer(text="Please try again later")
                    await ctx.message.clear_reaction(loading)
                    return await ctx.send(embed=embed)
                userdata = json.loads(await data.text())
                if not userdata["success"]:
                    await ctx.message.clear_reaction(loading)
                    return await ctx.reply(userdata["error"])
    userdata = userdata["data"]
    username = userdata["username"]
    clan = userdata["clan"]
    if not found:
        if clan == "VNTA":
            bgdata = bot.bgdata["vntasam123"]
        else:
            bgdata = {'file': 'https://media.discordapp.net/attachments/856723935357173780/856731786456858684/unknown.png',
             'hd': [255, 123, 57], 'st': [222, 222, 222], 'mt': '#vantalizing', 'us': [36, 36, 36], 'ov': True}
    kills = userdata["kills"]
    deaths = userdata["deaths"]
    kr = userdata["funds"]
    datestr = userdata["createdAt"].split("T")[0]
    wins = userdata["wins"]
    score = userdata["score"]
    level = userdata["level"]
    played = userdata["games"]
    loses = played - wins
    challenge = userdata.get("challenge")
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
    if kills == 0: mpk = "{:.2f}".format((shots - hits)/1)
    else: mpk = "{:.2f}".format((shots - hits) / kills)
    if hits == 0: hps = "{:.2f}%".format((headshots/1)*100)
    else: hps = "{:.2f}%".format((headshots/hits)*100)
    if nukes == 0: gpn = "{:.2f}".format(played/1)
    else: gpn = "{:.2f}".format(played / nukes)
    if daysplayed == 0: npd = "{:.2f}".format(nukes/ 1)
    else: npd = "{:.2f}".format(nukes/ daysplayed)
    if played == 0: kpg = "{:.2f}".format(kills/1)
    else: kpg = "{:.2f}".format(kills/played)
    kpm = "{:.2f}".format(float(kpg)/4)
    if loses == 0: wl = "{:.2f}".format(wins/1)
    else: wl = "{:.2f}".format(wins/loses)
    if deaths == 0: kdr = "{:.4f}".format(kills/1)
    else: kdr = "{:.4f}".format(kills / deaths)
    if kills == 0: spk = "{:.2f}".format(score/1)
    else: spk = "{:.2f}".format(score / kills)
    if played == 0: avgscore = int(score/1)
    else: avgscore = int(score / played)
    if shots == 0: accuracy = "{:.2f}%".format((hits/1)*100)
    else: accuracy = "{:.2f}%".format((hits/shots)*100)
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
        bgdata["file"] = 'https://media.discordapp.net/attachments/856723935357173780/856731786456858684/unknown.png'
    if userdata["hacker"]:
        bgdata["file"] = "https://media.discordapp.net/attachments/865932222577115146/867999500252381194/image_13.png"
        bgdata['hd'] = [255, 121, 121]
        bgdata['st'] = [183, 183, 183]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(bgdata["file"]) as r:
                imgtype = bgdata['file'].lower()[-3:]
                if r.status == 200:
                    with open(f"bgs/{ctx.author.id}.{imgtype}", 'wb') as f:
                        f.write(await r.read())
                else: raise ValueError
                bgimage = Image.open(f"bgs/{ctx.author.id}.{imgtype}")
    except Exception as error:
        bot.bgdata[ign]["file"] = ""
        await savebgdata()
        await ctx.message.clear_reaction(loading)
        return await ctx.reply(f"Background Corrupted. It is auto-removed. Please set again using `v.pbg`")
    if imgtype == "png":
        bgimage = bgimage.convert("RGBA").resize((1280, 720))
    hours, remainder = divmod(int(timeplayed), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    order = [[score, kills, deaths, kr, f"{days}d {hours}h {minutes}m", nukes],
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
                user = bot.get_user(int(key))
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
    await ctx.message.clear_reaction(loading)
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
                        else:
                            async with aiohttp.ClientSession(auto_decompress=False) as session:
                                async with session.get(image) as r:
                                    if r.status == 200:
                                        with open(f"bgs/{ctx.author.id}.png", 'wb') as f:
                                            f.write(await r.read())
                                        bgfile = await bot.get_channel(856723935357173780).send(
                                            file=discord.File(f"bgs/{ctx.author.id}.{image[-3:].lower()}",
                                                              filename=f"{ctx.author.id}.{image[-3:].lower()}"))
                                        bot.unsaved["vntasam123"]["file"] = bgfile.attachments[0].url
                                await ctx.send(f"Done!")
                                await sendnew(ctx, bot.unsaved["vntasam123"], "AwesomeSam")
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
                            h = msg.content.lower()
                            r, g, b = ImageColor.getcolor(h, "RGB")
                        else:
                            r, g, b = msg.content.replace(" ", "").split(",")
                        r = int(r)
                        g = int(g)
                        b = int(b)
                        if (r>255 or r<0) or (g>255 or g<0) or (b>255 or b<0): raise ValueError

                        types = {2: "hd", 3: "st", 5: "us", 6:"bt"}
                        bot.unsaved["vntasam123"][types[int(msgc[-1])]] = [r, g, b]
                        await ctx.send("Done!")
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
    #return await ctx.reply("Command Deleted")
    if bot.pause: return await ctx.send("⚠ ️Maintainence Update. Please retry later")
    if ign is not None and ctx.author.id in devs:
        ign = {"main":ign}
    else:
        ign = bot.links.get(str(ctx.author.id))
    if ign is None:
        return await ctx.reply("You need to be linked to get a custom background")
    ign = ign["main"].lower()
    if bot.apidown:
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        return await ctx.send(embed=embed)
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
                    embed = discord.Embed(description="Upload the `PNG` file from your PC to set as background.\n"
                                                      "**Dont send a link to the image! Upload the file**",
                                          color=embedcolor)
                    embed.set_footer(text="Recommended Size: 1280x720")
                    await ctx.send(embed=embed)

                    msg = await bot.wait_for("message", check=check, timeout=180)
                    try:
                        image = msg.attachments[0].url
                        if image[-3:].lower() not in ["png"]:
                            await ctx.send(f"{ctx.author.mention} The image should be `.PNG` file only!")
                            continue
                        else:
                            async with aiohttp.ClientSession(auto_decompress=False) as session:
                                async with session.get(image) as r:
                                    if r.status == 200:
                                        with open(f"bgs/{ctx.author.id}.{image[-3:].lower()}", 'wb') as f:
                                            f.write(await r.read())
                                        bgfile = await bot.get_channel(856723935357173780).send(
                                            file=discord.File(f"bgs/{ctx.author.id}.{image[-3:].lower()}",
                                                              filename=f"{ctx.author.id}.{image[-3:].lower()}"))
                                        bot.unsaved[ign]["file"] = bgfile.attachments[0].url
                                await ctx.send(f"Done!")
                                await sendnew(ctx, bot.unsaved[ign], ign)
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
                            h = msg.content.lower()
                            r, g, b = ImageColor.getcolor(h, "RGB")
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

@bot.command(aliases=["color"])
@commands.check(general)
async def colour(ctx, *args):
    msg = ctx.message
    msg.content = msg.content[len(ctx.invoked_with)+3:]

    if msg.content[0] == "#":
        h = msg.content.lower()
        r, g, b = ImageColor.getcolor(h, "RGB")
    else:
        r, g, b = msg.content.replace(" ", "").split(",")
    r = int(r)
    g = int(g)
    b = int(b)
    if (r > 255 or r < 0) or (g > 255 or g < 0) or (b > 255 or b < 0):
        return await ctx.reply("Invalid Color")
    hex_code = '%02x%02x%02x' % (r, g, b)
    embedc = int(hex_code, 16)
    embed = discord.Embed(title="Color",
                          description=f"RGB Code: {r}, {g}, {b}\n"
                                      f"Hex Code: #{hex_code}",
                          color=embedc)
    image = "https://media.discordapp.net/attachments/856723935357173780/865090200144052284/vnta_logo_png.png"
    async with aiohttp.ClientSession(auto_decompress=False) as session:
        async with session.get(image) as f:
            if f.status == 200:
                with open(f"logo.png", 'wb') as k:
                    k.write(await f.read())

    image = Image.open("logo.png")
    pixdata = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixdata[x, y] = tuple(list((r, g, b)) + [pixdata[x, y][-1]])
    image_bytes = BytesIO()
    image.save(image_bytes, 'PNG', transparent=True)
    image_bytes.seek(0)
    embed.set_thumbnail(url="attachment://logo.png")
    await ctx.send(embed=embed, file=discord.File(image_bytes, filename=f"logo.png"))

@bot.command()
@commands.check(general)
async def alts(ctx, mem:discord.Member=None):
    if mem is None:
        aut = ctx.author
        d = bot.links.get(str(ctx.author.id))
    else:
        aut = mem
        d = bot.links.get(str(mem.id))
    if d is None:
        return await ctx.send("You have no accounts linked. Use `v.link <ign>` to link an account first")
    else:
        work = bot.userdata.get(str(aut.id), {"incognito": False})["incognito"]
        if work and ctx.author.id != int(mem.id):
            return await ctx.send("You have no accounts linked. Use `v.link <ign>` to link an account first")
    altslist = "\n".join(list(set(d["all"])))
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
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id in devs:
        pass
    else:
        return
    server = await get_admin()
    if channel.id in server:
        embed = discord.Embed(description=f'{economyerror} {channel.mention} is already in list of registered channels!', color=error_embed)
        return await ctx.send(embed=embed)
    server.append(channel.id)
    if ctx.channel.id not in server:
        server.append(ctx.channel.id)
    bot.refr["719946380285837322"] = server
    await close_admin()
    embed = discord.Embed(description=f'{economysuccess} {channel.mention} added to list of registered channels successfully!', color=success_embed)
    await ctx.send(embed=embed)

@bot.command(aliases=['rem_chl', 'remove_chl', 'delete_chl'])
@commands.check(general)
async def del_chl(ctx, channel:discord.TextChannel):
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id in devs:
        pass
    else:
        return
    server = await get_admin()
    if channel.id not in server:
        embed = discord.Embed(description=f'{economyerror} {channel.mention} not in list of registered channels!', color=error_embed)
        return await ctx.send(embed=embed)
    server.remove(channel.id)
    bot.refr["719946380285837322"] = server
    await close_admin()
    embed = discord.Embed(description=f'{economysuccess} {channel.mention} removed from list of registered channels successfully!', color=success_embed)
    await ctx.send(embed=embed)

@bot.command(aliases=['show_chl'])
@commands.check(general)
async def list_chl(ctx):
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id in devs:
        pass
    else:
        return
    server = await get_admin()
    if len(server) == 0: channels = ['> No channels set']
    else: channels = [f'> <#{x}>' for x in server]
    embed = discord.Embed(title=f'{economysuccess} Allowed Channels for the bot:', description='\n'.join(channels), color=embedcolor)
    embed.set_footer(text='Add a channel using v.set_chl <name>\nRemove a channel using v.del_chl <name>')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(general)
async def reset_chl(ctx):
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id in devs: pass
    else: return
    server = await get_admin()
    embed = discord.Embed(title=f'{economysuccess} Done', description='Cleared Successfully!', color=embedcolor)
    bot.refr["719946380285837322"] = server
    await close_admin()
    embed.set_footer(text='Add a channel using e.set_chl <name>\nRemove a channel using e.del_chl <name>')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(general)
async def ping(ctx):
    msg = await ctx.send('Pinging Bot...')
    ping = "{:.2f} ms".format(bot.latency*1000)
    await msg.edit(content=f'Pong!\n'
                           f'Bot: `{ping}`\n'
                           f'Pinging Web Server...')
    t1 = time.time()
    a = requests.get("https://vntaweb.herokuapp.com/ping")
    if a.status_code == 200:
        pingtime = "{:.2f} ms".format((time.time() - t1)*1000)
    else:
        pingtime = "Unreachable"
    await msg.edit(content=f'Pong!\n'
                           f'Bot: `{ping}`\n'
                           f'Web: `{pingtime}`')

@bot.command(aliases=["app"])
async def application(ctx):
    if ctx.author.id not in staff: return
    embed = discord.Embed(title="VNTA Applications",
                          description="Click on the button below to start the application process!",
                          color=localembed)
    await ctx.send(view=PersistentView(), embed=embed)
    try:
        await ctx.author.send(f"You have successfully setup Applications in {ctx.channel.id}.\n"
                              f"Please DO NOT use the command again, as it will stop the current applications.\n"
                              f"If you want to change the channel, or re-use the command, tell {bot.dev.mention} beforehand.\n\n"
                              f"**PLEASE DO NOT RUN `v.app` AGAIN!**")
    except: pass
    bot.add_view(PersistentView())

async def pubs(data):
    kdr_req = bot.refr["pubs_con"]["kdr"]
    level_req = bot.refr["pubs_con"]["level"]
    kpg_req = bot.refr["pubs_con"]["kpg"]
    nukes_req = bot.refr["pubs_con"]["nukes"]
    a_open = bot.refr["pubs_con"]["open"]
    if data.user.id in bot.interlist:
        a = await data.response.send_message("You recently applied before. Please wait before re-applying", ephemeral=True)
        return

    if not a_open:
        await data.response.send_message("Pubstomper applications are closed", ephemeral=True)
        return
    try:
        test = await data.user.send("DM Testing")
        await test.delete()
        a = await data.response.send_message("Application process started in DMs", ephemeral=True)
    except Exception as e:
        print(e)
        return await data.response.send_message("Please open your DMs for starting the process", ephemeral=True)
    user = data.user
    if str(user.id) not in bot.links:
        await user.send("You are not linked to VNTA bot. Please go to <#813437412071440394> and type `v.link <your ign>`.\n"
                        "After linking, you can restart this process from <#813727689646538762>")
        return
    ign = bot.links.get(str(user.id))['main']
    embed = discord.Embed(title="Pubstomper Application",
                          description=f"Welcome to VNTA Application Process! Please follow the steps below for a smooth & troublefree experience\n"
                                      f"You are applying for your account- `{ign}`.\n"
                                      f"**Type `c` to confirm.**",
                          colour=localembed)
    embed.set_footer(text="The bot takes your main account to consideration.\nSet it using 'v.main <ign>'")
    await user.send(embed=embed)
    def check(msg):
        return msg.author == user and msg.guild is None

    try:
        msg = await bot.wait_for("message", check=check, timeout=180)
        res = msg.content.lower()
        if res == "c":
            asyncio.create_task(timeout(user))
        else:
            return await user.send("Application Aborted")
    except asyncio.TimeoutError:
        return await user.send("You didnt reply in time.")

    fetch = await user.send("Fetching Stats, Hang on..")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
            if data.status != 200:
                embed = discord.Embed(title=f"{economyerror} Error",
                                      description="Failed to fetch automatically: API didnt respond in time",
                                      color=error_embed)
                await fetch.edit(embed=embed)
            else:
                userdata = json.loads(await data.text())
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
                timeplayed = int(userdata["timePlayed"] / 1000)
                melee = userdata["stats"].get("mk", 0)
                wallbangs = userdata["stats"].get("wb", 0)
                date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d')
                now = datetime.datetime.now()
                daysplayed = (now - date_obj).days
                mpk = "{:.2f}".format((shots - hits) / kills)
                hps = "{:.2f}%".format((headshots / hits) * 100)
                gpn = "{:.2f}".format(played / nukes)
                npd = "{:.2f}".format(nukes / daysplayed)
                kpg = "{:.2f}".format(kills / played)
                kpm = "{:.2f}".format(float(kpg) / 4)
                if loses == 0: loses = 1
                wl = "{:.2f}".format(wins / loses)
                kdr = "{:.4f}".format(kills / deaths)
                spk = "{:.2f}".format(score / kills)
                avgscore = int(score / played)
                accuracy = "{:.2f}%".format((hits / shots) * 100)

                score = 0
                economysuccess = "✔️"
                embed = discord.Embed(title=f"{username}", color=localembed)
                if level >= level_req:
                    mark = economysuccess
                    score += 1
                else:
                    mark = economyerror
                    score -= 2
                embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

                if float(kdr) >= kdr_req:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

                if float(kpg) >= kpg_req:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

                if nukes >= nukes_req:
                    mark = economysuccess
                    score += 1
                else:
                    mark = economyerror
                    score -= 2
                embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)

                p = False
                if 2 <= score <= 4:
                    res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
                    p = True
                else: res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
                embed.add_field(name="Result", value=res, inline=False)
                rescode = hex(random.randint(1000, 9999)).lower()
                allapps = bot.refr.setdefault("apps", [])
                allapps.append({rescode:{"type":"pubs", "kdr":kdr, "level":level, "kpg":kpg, "username":username, "nukes":nukes}})
                bot.refr["apps"] = allapps
                await close_admin()
                if p:
                    aft = bot.get_guild(719946380285837322).get_role(835545980811870218)
                    await bot.get_guild(719946380285837322).get_member(user.id).add_roles(aft)
                    embed.add_field(name="If you wish to continue:", value=f"Head over to <#848532015270854668>, and click on 📩 to create a ticket.\n"
                                                                           f"After opening of the ticket, type `v.result {rescode}` in **your ticket channel.**\n"
                                                                           f" The staff will guide you after that.",
                                    inline=False)
                embed.set_footer(text="#vantalizing")
                embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/l8ile3RBeJ7FZELTOiecL6LMUQz5qmExL8ELzQFuEag/https/media.discordapp.net/attachments/817374020810178583/838450855648690226/vnta_logo_png.png")
                await fetch.edit(embed=embed, content=None)

async def cc(data):
    a_open = bot.refr["cc_con"]["open"]
    if data.user.id in bot.interlist:
        a = await data.response.send_message("You recently applied before. Please wait before re-applying",
                                             ephemeral=True)
        return

    if not a_open:
        await data.response.send_message("CC applications are closed", ephemeral=True)
        return
    try:
        test = await data.user.send("DM Testing")
        await test.delete()
        await data.response.send_message("Application process started in DMs", ephemeral=True)
    except:
        return await data.response.send_message("Please open your DMs for starting the process", ephemeral=True)
    user = data.user
    try:
        embed = discord.Embed(title="Note!",
                              description=f"Please make sure you have your YouTube and Twitch account linked to your discord",
                              color=localembed)
        embed.set_footer(text="React below to continue")
        em = await user.send(embed=embed)
        await em.add_reaction(economysuccess)

        def check(reaction, user_):
            return user_ == user and str(reaction.emoji) == economysuccess

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        asyncio.create_task(timeout(user))
        embed = discord.Embed(title="Step I",
                              description="Please authorize to the bot here: [Auth URL](https://vntaweb.herokuapp.com/)",
                              colour=localembed)
        embed.set_footer(text="When done, react below to confirm")
        em = await user.send(embed=embed)
        await em.add_reaction(economysuccess)

        reaction, user_ = await bot.wait_for('reaction_add', timeout=180, check=check)
        await em.add_reaction(loading)
        yt, twitch = False, False
        usercons = bot.refr["con"].get(str(user.id), [])

        for cons in usercons:
            if cons["type"] == "youtube": yt = True
            if cons["type"] == "twitch": twitch = True
        if (not yt) and (not twitch):
            return await user.send("You do not have YouTube or Twitch linked. Please link them and try again")
        ytvids = []
        twitchdata = {}
        subcount = 0
        thumburl = ""
        if yt:
            for k in usercons:
                if k["type"] == "youtube": chlid = k["id"]
            uri = f"https://www.googleapis.com/youtube/v3/channels?id={chlid}&key={YT_API_KEY}&part=contentDetails"
            a = requests.get(uri)
            data = json.loads(a.text)
            uploadsid = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            uri4 = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={chlid}&key={YT_API_KEY}"
            d = requests.get(uri4)
            data2 = json.loads(d.text)
            items = data2["items"][0]["statistics"]
            if items["hiddenSubscriberCount"]: subcount = "Hidden"
            else: subcount = items["subscriberCount"]

            uri5 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={chlid}&fields=items%2Fsnippet%2Fthumbnails&key={YT_API_KEY}"
            e = requests.get(uri5)
            data3 = json.loads(e.text)
            thumburl = data3["items"][0]["snippet"]["thumbnails"]["medium"]["url"]

            uri2 = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={uploadsid}&key={YT_API_KEY}"
            b = requests.get(uri2)
            vids = json.loads(b.text)
            vids_c = vids["items"]

            for i in vids_c:
                vidid = i["contentDetails"]["videoId"]
                uri3 = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={vidid}&key={YT_API_KEY}"
                res = requests.get(uri3)
                viddetail = json.loads(res.text)
                viddetail = viddetail["items"][0]["statistics"]

                datadict = {"name":i["snippet"]["title"],
                            "publish":i["snippet"]["publishedAt"],
                            "views":int(viddetail["viewCount"]),
                            "likes":int(viddetail["likeCount"]),
                            "dislikes":int(viddetail["dislikeCount"]),
                            "comments":int(viddetail["commentCount"]),
                            "url":f"https://youtube.com/watch?v={vidid}"
                            }
                ytvids.append(datadict)
        if twitch:
            for k in usercons:
                if k["type"] == "twitch": chlid = k["id"]
            if bot.twitchapi["expiry"] < time.time():
                print("Requesting new token...")
                a = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")
                res = json.loads(a.text)
                bot.twitchapi["token"] = res["access_token"]
                bot.twitchapi["expiry"] = time.time() + res["expires_in"]
            header = {'Authorization': f'Bearer {bot.twitchapi["token"]}', 'Client-Id': CLIENT_ID}

            url = f"https://api.twitch.tv/helix/users?id={chlid}"
            a = requests.get(url, headers=header)
            data = json.loads(a.text)
            data = data["data"][0]
            twitchdata["pfp"] = data["profile_image_url"]
            twitchdata["name"] = data["display_name"]
            twitchdata["views"] = data["view_count"]

            url2 = f"https://api.twitch.tv/helix/users/follows?to_id={chlid}"
            b = requests.get(url2, headers=header)
            data2 = json.loads(b.text)
            twitchdata["followers"] = data2["total"]

            url3 = f"https://api.twitch.tv/helix/videos?user_id={chlid}"
            c = requests.get(url3, headers=header)
            data3 = json.loads(c.text)
            twitchdata["data"] = data3["data"]

        embed = discord.Embed(title=f"Success", color=localembed)

        rescode = hex(random.randint(10000, 99999)).lower()
        allapps = bot.refr.setdefault("apps", [])
        allapps.append({rescode: {"type":"cc",
                                  "yt": {"linked":yt, "data":ytvids, "thumbnail":thumburl, "subs":subcount, "url":f"https://www.youtube.com/channel/{chlid}"},
                                  "twitch":{"linked":twitch, "data":twitchdata}}})
        bot.refr["apps"] = allapps
        await close_admin()
        await em.remove_reaction(loading, bot.user)
        aft = bot.get_guild(719946380285837322).get_role(835545980811870218)
        await bot.get_guild(719946380285837322).get_member(user.id).add_roles(aft)
        embed.add_field(name="If you wish to continue:",
                        value=f"Head over to <#848532015270854668>, and click on 📩 to create a ticket.\n"
                              f"After opening of the ticket, type `v.result {rescode}` in **your ticket channel.**\n"
                              f" The staff will guide you after that.",
                        inline=False)
        embed.set_footer(text="#vantalizing")
        embed.set_thumbnail(
            url="https://images-ext-2.discordapp.net/external/l8ile3RBeJ7FZELTOiecL6LMUQz5qmExL8ELzQFuEag/https/media.discordapp.net/attachments/817374020810178583/838450855648690226/vnta_logo_png.png")
        await user.send(embed=embed)
    except Exception as e: print(e)

async def comp(data):
    kdr_req = bot.refr["comp_con"]["kdr"]
    level_req = bot.refr["comp_con"]["level"]
    kpg_req = bot.refr["comp_con"]["kpg"]
    nukes_req = bot.refr["comp_con"]["nukes"]
    a_open = bot.refr["comp_con"]["open"]
    if data.user.id in bot.interlist:
        a = await data.response.send_message("You recently applied before. Please wait before re-applying",
                                             ephemeral=True)
        return

    if not a_open:
        await data.response.send_message("Competitive applications are closed", ephemeral=True)
        return
    try:
        test = await data.user.send("DM Testing")
        await test.delete()
        a = await data.response.send_message("Application process started in DMs", ephemeral=True)
    except Exception as e:
        print(e)
        return await data.response.send_message("Please open your DMs for starting the process", ephemeral=True)
    user = data.user
    if str(user.id) not in bot.links:
        await user.send("You are not linked to VNTA bot. Please go to <#813437412071440394> and type `v.link <your ign>`.\n"
                        "After linking, you can restart this process from <#813727689646538762>")
        return
    ign = bot.links.get(str(user.id))['main']
    embed = discord.Embed(title="Competitive Application",
                          description=f"Welcome to VNTA Application Process! Please follow the steps below for a smooth & troublefree experience\n"
                                      f"You are applying for your account- `{ign}`.\n"
                                      f"**Type `c` to confirm.**",
                          colour=localembed)
    embed.set_footer(text="The bot takes your main account to consideration.\nSet it using 'v.main <ign>'")
    await user.send(embed=embed)
    def check(msg):
        return msg.author == user and msg.guild is None

    try:
        msg = await bot.wait_for("message", check=check, timeout=180)
        res = msg.content.lower()
        if res == "c":
            asyncio.create_task(timeout(user))
        else:
            return await user.send("Application Aborted")
    except asyncio.TimeoutError:
        return await user.send("You didnt reply in time.")

    fetch = await user.send("Fetching Stats, Hang on..")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://kr.vercel.app/api/profile?username={ign}") as data:
            if data.status != 200:
                embed = discord.Embed(title=f"{economyerror} Error",
                                      description="Failed to fetch automatically: API didnt respond in time",
                                      color=error_embed)
                await fetch.edit(embed=embed)
            else:
                userdata = json.loads(await data.text())
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
                timeplayed = int(userdata["timePlayed"] / 1000)
                melee = userdata["stats"].get("mk", 0)
                wallbangs = userdata["stats"].get("wb", 0)
                date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d')
                now = datetime.datetime.now()
                daysplayed = (now - date_obj).days
                mpk = "{:.2f}".format((shots - hits) / kills)
                hps = "{:.2f}%".format((headshots / hits) * 100)
                gpn = "{:.2f}".format(played / nukes)
                npd = "{:.2f}".format(nukes / daysplayed)
                kpg = "{:.2f}".format(kills / played)
                kpm = "{:.2f}".format(float(kpg) / 4)
                if loses == 0: loses = 1
                wl = "{:.2f}".format(wins / loses)
                kdr = "{:.4f}".format(kills / deaths)
                spk = "{:.2f}".format(score / kills)
                avgscore = int(score / played)
                accuracy = "{:.2f}%".format((hits / shots) * 100)

                score = 0
                economysuccess = "✔️"
                embed = discord.Embed(title=f"{username}", color=localembed)
                if level >= level_req:
                    mark = economysuccess
                    score += 1
                else:
                    mark = economyerror
                    score -= 2
                embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

                if float(kdr) >= kdr_req:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

                if float(kpg) >= kpg_req:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

                if nukes >= nukes_req:
                    mark = economysuccess
                    score += 1
                else:
                    mark = economyerror
                    score -= 2
                embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)

                p = False
                if 2 <= score <= 4:
                    res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
                    p = True
                else: res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
                embed.add_field(name="Result", value=res, inline=False)
                rescode = hex(random.randint(1000, 9999)).lower()
                allapps = bot.refr.setdefault("apps", [])
                allapps.append({rescode:{"type":"comp", "kdr":kdr, "level":level, "kpg":kpg, "username":username, "nukes":nukes}})
                bot.refr["apps"] = allapps
                await close_admin()
                if p:
                    aft = bot.get_guild(719946380285837322).get_role(835545980811870218)
                    await bot.get_guild(719946380285837322).get_member(user.id).add_roles(aft)
                    embed.add_field(name="Follow the steps below:",
                                    value=f"Head over to <#848532015270854668>, and click on 📩 to create a ticket.\n"
                                          f"After opening of the ticket, type `v.result {rescode}` in **your ticket channel.**\n"
                                          f" The staff will guide you after that.",
                                    inline=False)
                embed.set_footer(text="#vantalizing")
                embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/l8ile3RBeJ7FZELTOiecL6LMUQz5qmExL8ELzQFuEag/https/media.discordapp.net/attachments/817374020810178583/838450855648690226/vnta_logo_png.png")
                await fetch.edit(embed=embed, content=None)

async def configpubs(ctx):
    bot.refr.setdefault("pubs_con", {})
    kdr = bot.refr["pubs_con"].get("kdr", 4)
    level = bot.refr["pubs_con"].get("level", 60)
    kpg = bot.refr["pubs_con"].get("kpg", 16)
    nukes = bot.refr["pubs_con"].get("nukes", 100)
    a_open = bot.refr["pubs_con"].get("open", True)
    if a_open: ifopen = "Yes"
    else: ifopen = "No"

    embed = discord.Embed(title="Pubstomper Configuration",
                          description="Type `modify <s.no>` to change that field's value", color=localembed)
    embed.add_field(name="1. Application Open", value=ifopen, inline=False)
    embed.add_field(name="2. Level", value=level, inline=False)
    embed.add_field(name="3. KDR", value=kdr, inline=False)
    embed.add_field(name="4. KPG", value=kpg, inline=False)
    embed.add_field(name="5. Nukes", value=nukes, inline=False)
    embed.set_footer(text="Type 'cancel' to cancel changes\n"
                          "Type 'save' to save all the changes")
    newdict = {"kdr":kdr, "kpg":kpg, "level":level, "nukes":nukes, "open":a_open}
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
            cont = msg.content.lower()

            if cont == "modify 1":
                if a_open: a_open = False
                else: a_open = True
                await msg.add_reaction(economysuccess)
            if cont == "modify 2":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: level = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 3":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: kdr = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 4":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: kpg = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 5":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: nukes = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "cancel": return
            if cont == "save":
                bot.refr["pubs_con"] = newdict
                await close_admin()
                await ctx.send(f"{economysuccess} Saved all the changes")
                return
            newdict = {"kdr": kdr, "kpg": kpg, "level": level, "nukes": nukes, "open": a_open}
        except:
            pass

async def configcomp(ctx):
    bot.refr.setdefault("comp_con", {})
    kdr = bot.refr["comp_con"].get("kdr", 4)
    level = bot.refr["comp_con"].get("level", 40)
    kpg = bot.refr["comp_con"].get("kpg", 16)
    nukes = bot.refr["comp_con"].get("nukes", 100)
    a_open = bot.refr["comp_con"].get("open", True)
    if a_open: ifopen = "Yes"
    else: ifopen = "No"

    embed = discord.Embed(title="Competitive Configuration",
                          description="Type `modify <s.no>` to change that field's value", color=localembed)
    embed.add_field(name="1. Application Open", value=ifopen, inline=False)
    embed.add_field(name="2. Level", value=level, inline=False)
    embed.add_field(name="3. KDR", value=kdr, inline=False)
    embed.add_field(name="4. KPG", value=kpg, inline=False)
    embed.add_field(name="5. Nukes", value=nukes, inline=False)
    embed.set_footer(text="Type 'cancel' to cancel changes\n"
                          "Type 'save' to save all the changes")
    newdict = {"kdr":kdr, "kpg":kpg, "level":level, "nukes":nukes, "open":a_open}
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
            cont = msg.content.lower()

            if cont == "modify 1":
                if a_open: a_open = False
                else: a_open = True
                await msg.add_reaction(economysuccess)
            if cont == "modify 2":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: level = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 3":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: kdr = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 4":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: kpg = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "modify 5":
                await ctx.send("Enter the new value")
                newmsg = await bot.wait_for("message", check=check, timeout=60)
                try: nukes = int(newmsg.content); await newmsg.add_reaction(economysuccess)
                except: await ctx.send("Incorrect Value")
            if cont == "save":
                bot.refr["comp_con"] = newdict
                await close_admin()
                await ctx.send(f"{economysuccess} Saved all the changes")
                return
            if cont == "cancel": return
            newdict = {"kdr": kdr, "kpg": kpg, "level": level, "nukes": nukes, "open": a_open}
        except:
            pass

async def configcc(ctx):
    bot.refr.setdefault("cc_con", {})
    a_open = bot.refr["cc_con"].get("open", True)
    if a_open: ifopen = "Yes"
    else: ifopen = "No"

    embed = discord.Embed(title="CC Configuration",
                          description="Type `modify <s.no>` to change that field's value", color=localembed)
    embed.add_field(name="1. Application Open", value=ifopen, inline=False)
    embed.set_footer(text="Type 'cancel' to cancel changes\n"
                          "Type 'save' to save all the changes")
    newdict = {"open":a_open}
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
            cont = msg.content.lower()

            if cont == "modify 1":
                if a_open: a_open = False
                else: a_open = True
                await msg.add_reaction(economysuccess)
            if cont == "cancel": return
            if cont == "save":
                bot.refr["cc_con"] = newdict
                await close_admin()
                await ctx.send(f"{economysuccess} Saved all the changes")
                return
            newdict = {"open": a_open}
        except:
            pass

@bot.command(aliases=["appc"])
async def appconfig(ctx):
    if ctx.author.id not in staff: return
    embed = discord.Embed(title="⚙️ Configuration",
                          description="**Select the option below:**\n\n"
                                      "1\N{variation selector-16}\N{combining enclosing keycap} Pubstomper\n"
                                      "2\N{variation selector-16}\N{combining enclosing keycap} Competitive\n"
                                      "3\N{variation selector-16}\N{combining enclosing keycap} Content Creator",
                          color=localembed)
    a = await ctx.send(embed=embed)
    await a.add_reaction("1\N{variation selector-16}\N{combining enclosing keycap}")
    await a.add_reaction("2\N{variation selector-16}\N{combining enclosing keycap}")
    await a.add_reaction("3\N{variation selector-16}\N{combining enclosing keycap}")

    def check(reaction, user):
        return user == ctx.author

    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

    if str(reaction.emoji) == "1\N{variation selector-16}\N{combining enclosing keycap}":
        await configpubs(ctx)
    elif str(reaction.emoji) == "2\N{variation selector-16}\N{combining enclosing keycap}":
        await configcomp(ctx)
    elif str(reaction.emoji) == "3\N{variation selector-16}\N{combining enclosing keycap}":
        await configcc(ctx)

@bot.command()
@commands.is_owner()
async def emoji(ctx, link, name):
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        a = r.content
        """with open(f"{name}.png", 'wb') as f:
            shutil.copyfileobj(r.raw, f)"""
        await ctx.guild.create_custom_emoji(name=name, image=a)

@bot.command()
@commands.check(general)
async def result(ctx, code):
    if "ticket" not in ctx.channel.name:
        return await ctx.reply("Resut can be viewed in tickets created via <#848532015270854668> only.")
    apps = bot.refr.get("apps", [])
    found = False
    userapp = {}
    for j in apps:
        for i in j.items():
            if i[0] == code.lower():
                userapp = i[1]
                found = True
                break
        if found:
            apps.remove(j)
            bot.refr["apps"] = apps
            await close_admin()
            break
    if not found:
        return await ctx.reply("Invalid code or ticket already opened")
    await ctx.message.delete()

    score = 0
    economysuccess = "✔️"
    embedslist = []
    if userapp["type"] == "pubs":
        kdr_req = bot.refr["pubs_con"]["kdr"]
        level_req = bot.refr["pubs_con"]["level"]
        kpg_req = bot.refr["pubs_con"]["kpg"]
        nukes_req = bot.refr["pubs_con"]["nukes"]

        level = userapp["level"]
        kdr = userapp["kdr"]
        kpg = userapp["kpg"]
        nukes = userapp["nukes"]

        embed = discord.Embed(title=f'{userapp["username"]} | Pubstomper Application', colour=localembed, url=f"https://kr.social/p/{userapp['username']}")
        if level >= level_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

        if float(kdr) >= kdr_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

        if float(kpg) >= kpg_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

        if nukes >= nukes_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)
        if 2 <= score <= 4:
            res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
        else:
            res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
        embed.add_field(name="Result", value=res)
        embedslist.append(embed)
    elif userapp["type"] == "cc":
        yt = userapp["yt"]
        if yt["linked"]:
            count = len(yt["data"])
            embed = discord.Embed(title="<:YouTube:865575628710608916> YouTube", colour=localembed, url=yt["url"])
            embed.set_thumbnail(url=yt["thumbnail"])
            embed.add_field(name="Total Videos", value=count)
            embed.add_field(name="Subscribers", value=yt["subs"])
            embed.add_field(name="\u200b", value="\u200b")
            views, likes, dislikes = 0, 0, 0
            views_l, likes_l, dislikes_l = [], [], []
            for i in yt["data"]:
                views += i["views"]
                likes += i["likes"]
                dislikes += i["dislikes"]

                views_l.append(i["views"])
                likes_l.append(i["likes"])
                dislikes_l.append(i["dislikes"])
            embed.add_field(name="Average Views", value="{:.2f}".format(views/count))
            embed.add_field(name="Average Likes", value="{:.2f}".format(likes/count))
            embed.add_field(name="Average Dislikes", value="{:.2f}\n\u200b".format(dislikes/count))

            if len(views_l) != 0: max_views = max(views_l)
            else: max_views = 0
            if len(likes_l) != 0: max_likes = max(likes_l)
            else:
                max_likes = 0
            if len(dislikes_l) != 0: max_dislikes = max(dislikes_l)
            else:
                max_dislikes = 0
            for i in yt["data"]:
                if i["views"] == max_views: embed.add_field(name=f"Most Viewed:", value=f"[`{i['name']}`]({i['url']})\n"
                                                                                        f"**Views:** {max_views}\n"
                                                                                      f"**Likes:** {i['likes']}\n"
                                                                                      f"**Dislikes:** {i['dislikes']}\n"
                                                                                      f"**Comments:** {i['comments']}\n"
                                                                                      f"\u200b",
                                                            inline=False)
                if i["likes"] == max_likes: embed.add_field(name=f"Most Liked:", value=f"[`{i['name']}`]({i['url']})\n"
                                                                                       f"**Views:** {i['views']}\n"
                                                                                      f"**Likes:** {i['likes']}\n"
                                                                                      f"**Dislikes:** {i['dislikes']}\n"
                                                                                      f"**Comments:** {i['comments']}\n"
                                                                                      f"\u200b",
                                                            inline=False)
                if i["dislikes"] == max_dislikes: embed.add_field(name=f"Most Disliked:", value=f"[`{i['name']}`]({i['url']})\n"
                                                                                                f"**Views:** {i['views']}\n"
                                                                                      f"**Likes:** {i['likes']}\n"
                                                                                      f"**Dislikes:** {i['dislikes']}\n"
                                                                                      f"**Comments:** {i['comments']}\n"
                                                                                      f"\u200b",
                                                            inline=False)
            embedslist.append(embed)
        else:
            embed = discord.Embed(title="<:YouTube:865575628710608916> YouTube", colour=localembed,
                                  description="Not Linked")
            embedslist.append(embed)

        twi = userapp["twitch"]
        if twi["linked"]:
            twitchdata = twi["data"]
            embed = discord.Embed(title="<:Twitch:865575682208825355> Twitch", colour=localembed,
                                  url=f"https://twitch.tv/{twitchdata['name']}")
            embed.add_field(name="Name", value=twitchdata["name"])
            embed.add_field(name="Followers", value=twitchdata["followers"])
            embed.add_field(name="Total Views", value=twitchdata["views"])
            embed.add_field(name="Videos Found", value=len(twitchdata["data"]))
            views_l = []
            for vid in twitchdata["data"]:
                views_l.append(vid["view_count"])
            if len(views_l) != 0: maxview = max(views_l)
            else: maxview = 0

            for vid in twitchdata["data"]:
                if vid["view_count"] == maxview:
                    dur = vid["duration"]
                    splitted = dur.split("h")
                    hrs = splitted[0]
                    split2 = splitted[1].split("m")
                    mins = split2[0]

                    created = vid["created_at"].split("T")[0]
                    dtobj = datetime.datetime.strptime(created, "%Y-%m-%d")
                    timeobj = int(time.mktime(dtobj.timetuple()))
                    embed.add_field(name="Most Viewed:",
                                    value=f"[`{vid['title']}`]({vid['url']})\n"
                                          f"**Views:** {maxview}\n"
                                          f"**Duration:** `{hrs}h {mins}m`\n"
                                          f"**Streamed On:** <t:{timeobj}:D> (<t:{timeobj}:R>)")

            embed.set_thumbnail(url=twitchdata["pfp"])
            embedslist.append(embed)
        else:
            embed = discord.Embed(title="<:Twitch:865575682208825355> Twitch", colour=localembed,
                                  description="Not Linked")
            embedslist.append(embed)
    else:
        kdr_req = bot.refr["comp_con"]["kdr"]
        level_req = bot.refr["comp_con"]["level"]
        kpg_req = bot.refr["comp_con"]["kpg"]
        nukes_req = bot.refr["comp_con"]["nukes"]

        level = userapp["level"]
        kdr = userapp["kdr"]
        kpg = userapp["kpg"]
        nukes = userapp["nukes"]

        embed = discord.Embed(title=f'{userapp["username"]} | Competitive Application', colour=localembed,
                              url=f"https://kr.social/p/{userapp['username']}")
        if level >= level_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

        if float(kdr) >= kdr_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

        if float(kpg) >= kpg_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

        if nukes >= nukes_req:
            mark = economysuccess
            score += 1
        else:
            mark = economyerror
        embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)

        if 2 <= score <= 4:
            res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
        else:
            res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
        embed.add_field(name="Result", value=res)
        embedslist.append(embed)
    msg = await ctx.send(f"{ctx.author.mention}", embeds=embedslist)
    if userapp["type"] in ["pubs", "comp"]:
        await ctx.send("Kindly wait for a <@&813729487292334081> to respond.\n"
                        "In the meanwhile, please post the screenshot of your best game")
    await close_admin()

@bot.command(aliases=["rem", "rems", "reminders"])
@commands.check(general)
async def reminder(ctx, action=None, *args):
    if action is None:
        embed = discord.Embed(title="Reminders",
                              description="Set a reminder and let the bot DM/ping you. Never forget anything again!\n\n"
                                          "**Commands:**\n"
                                          "`v.rem add`  (for interactive setup)\n"
                                          "`v.rem show` (view all active reminders)\n"
                                          "`v.rem del <reminder-id>` (delete reminder)\n"
                                          "`v.rem del -a`             (delete all reminders)\n"
                                          "\n"
                                          "**For a quick reminder:** `v.remindme <time> [desc]`\n"
                                          "Example:\n"
                                          "- `v.remindme 5m switch off microwave`\n"
                                          "- `v.remindme 1h english class`\n"
                                          "- `v.remindme 2d5h announce smth`",
                              color=embedcolor)
        embed.set_thumbnail(url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
        return await ctx.send(embed=embed)
    if action.lower() == "show":
        aut = bot.refr["rems"].get(str(ctx.author.id))
        if aut is None or len(aut) == 0:
            embed = discord.Embed(title="Your Reminders",
                                  description="Nothing here. But its never too late to add a reminder!",
                                  color=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")

            return await ctx.send(embed=embed)
        embed = discord.Embed(title="Your Reminders",
                              color=localembed)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
        embed.set_thumbnail(
            url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
        for i in aut:
            hours, remainder = divmod(int(i["time"] - time.time() + i["tadd"]), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed.add_field(name=f"ID: {i['id']}", value=f"`Desc:` {i['desc']}\n"
                                                        f"`Time Left:` {days}d, {hours}h, {minutes}m, {seconds}s\n"
                                                        f"`Set at:` <t:{int(i['tadd'])}:F> (<t:{int(i['tadd'])}:R>)\n"
                                                        f"`End at:` <t:{int(i['time'] + i['tadd'])}:F> (<t:{int(i['time'] + i['tadd'])}:R>)", inline=False)
        await ctx.send(embed=embed)
    elif action.lower() == "add":
        try:
            embed = discord.Embed(title="Add a reminder",
                                  description="Enter the description for the reminder.\nFor empty description, type `skip`",
                                  color=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
            embed.set_thumbnail(url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
            em = await ctx.send(embed=embed)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await bot.wait_for("message", timeout=300, check=check)
            desc = msg.content
            if desc.lower() == "skip": desc = ""
            await msg.delete()
            embed = discord.Embed(title="Add a reminder",
                                  description="Enter the time duration from now. This should be in x**d**x**h**x**m**x**s**\n"
                                              "Examples:\n"
                                              "`1d5h`  => 1 day 5 hrs\n"
                                              "`5h10m` => 5 hrs 10 mins\n"
                                              "`5m30s` => 5 mins 30 secs",
                                  color=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
            await em.edit(embed=embed)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg_ = await bot.wait_for("message", timeout=300, check=check)
            msg = msg_.content.lower()

            secs = await conv_rem(msg)
            if secs == "error":
                return await ctx.send(f"{ctx.author.mention} Invalid time format!")
            remid = bot.refr.setdefault("rems_c", 100000)
            bot.refr["rems_c"] = remid + 1
            allrems = bot.refr.setdefault("rems", {})
            autrems = allrems.setdefault(str(ctx.author.id), [])
            autrems.append({"tadd":time.time(), "desc":desc, "time":secs, "id":remid+1, "chl":ctx.channel.id})
            allrems[str(ctx.author.id)] = autrems
            bot.refr["rems"] = allrems
            await msg_.delete()
            embed = discord.Embed(title="Add a reminder",
                                  description=f"Done! I will remind you at <t:{int(time.time() + secs)}:F> ;)",
                                  colour=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
            await em.edit(embed=embed)
            await close_admin()
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} You didn't reply in time. Reminder aborted")
    elif action.lower() in ["delete", "del"]:
        aut = bot.refr["rems"].get(str(ctx.author.id))
        if aut is None:
            embed = discord.Embed(title="Your Reminders",
                                  description="Nothing here. But its never too late to add a reminder!",
                                  color=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
            return await ctx.send(embed=embed)
        try:
            found = True
            argslist = []
            if any(["-a" in args, "-A" in args]):
                for i in aut:
                    aut.remove(i)
            else:
                index = 0
                argslist = [int(arg) for arg in args]
                newaut = copy.copy(aut)
                for i in newaut:
                    if i["id"] in argslist:
                        aut.remove(i)
                        argslist.remove(i["id"])

            bot.refr["rems"][str(ctx.author.id)] = aut
            await ctx.reply(f"{economysuccess} Reminder(s) Deleted")
            await close_admin()
            if len(argslist) != 0:
                raise NameError(", ".join([str(x) for x in argslist]))
        except NameError as e: await ctx.reply(f"Invalid Reminder ID(s): `{e}`")
        #except: return await ctx.reply("Invalid Reminder ID")
    else: await reminder(ctx)

@bot.command()
@commands.check(general)
async def remindme(ctx, rtime, *, desc=None):
    secs = await conv_rem(rtime.lower())
    if secs == "error":
        return await ctx.send(f"{ctx.author.mention} Invalid time format!")
    if desc is None: desc = ""
    remid = bot.refr["rems_c"]
    bot.refr["rems_c"] = remid + 1
    allrems = bot.refr["rems"]
    autrems = allrems.setdefault(str(ctx.author.id), [])
    autrems.append({"tadd": time.time(), "desc": desc, "time": secs, "id": remid + 1, "chl":ctx.channel.id})
    allrems[str(ctx.author.id)] = autrems
    bot.refr["rems"] = allrems
    embed = discord.Embed(title="Quick Reminder",
                          description=f"Done! I will remind you at <t:{int(time.time() + secs)}:F> ;)",
                          colour=localembed)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar.url)
    embed.set_thumbnail(
        url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")
    await ctx.send(embed=embed)
    await close_admin()

@bot.command(aliases=["tar"])
@commands.check(general)
async def target(ctx, kills:int, *, ign=None):
    await ctx.message.add_reaction(loading)
    if ign is not None:
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
    else:
        ign = bot.links.get(str(ctx.author.id))
        if ign is None:
            await ctx.message.clear_reaction(loading)
            return await ctx.reply("You are not linked. Use `v.link <ign>` to get linked")
        ign = ign["main"]
    if (kills <= 0) or (kills >= 4000):
        await ctx.message.clear_reaction(loading)
        return await ctx.reply("Smh you should stop playing with me and better do wars")
    data = await getdata("VNTA")
    if data == "error":
        embed = discord.Embed(title=f"{economyerror} Error",
                              description="API didnt respond in time",
                              color=error_embed)
        embed.set_footer(text="Please try again later")
        await ctx.message.clear_reaction(loading)
        return await ctx.send(embed=embed)
    data = data["data"]["members"]
    found = False
    for i in data:
        if ign.lower() == i["username"].lower():
            userdata = i
            con = i["contract"]
            found = True
            break
    if not found:
        await ctx.message.clear_reaction(loading)
        return await ctx.reply("User not in VNTA. Make sure that VNTA account is set as your main account")
    timeplayed = int(con["timeplayed"] / 1000)
    left = datetime.timedelta(seconds=timeplayed)
    if timeplayed > 10800:
        await ctx.message.clear_reaction(loading)
        return await ctx.reply("You have completed your contract")
    tleft = 10800 - timeplayed
    games = tleft / 240
    ckills = con["kills"]
    rem = kills - ckills
    if rem < 0:
        await ctx.message.clear_reaction(loading)
        return await ctx.reply("Target less that current kills")

    x = PrettyTable()
    x.field_names = ["Name", "Stats"]
    x.title = f"Target- {kills}"
    x.add_row(["Time left", "{:.2f} mins".format(games*4)])
    x.add_row(["Games left", "{:.2f}".format(games)])
    x.add_row(["Req. KPG", "{:.2f}".format(rem/games)])
    x.add_row(["Req. KPM", "{:.2f}".format((rem/games)/4)])
    await ctx.send(embed=discord.Embed(title=userdata["username"], description=f"```py\n{x}```", color=localembed))
    await ctx.message.clear_reaction(loading)

async def load_peeps():
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://kr.vercel.app/api/clan?clan=vnta", timeout=timeout) as a:
                if a.status != 200:
                    bot.apidown = True
                    return
                bot.apidown = False
                data = json.loads(await a.text())
                bot.vntapeeps.clear()
                for i in data["data"]["members"]:
                    bot.vntapeeps.append(i["username"].lower())
    except: pass

@bot.command()
@commands.is_owner()
async def pause(ctx):
    if bot.pause: bot.pause = False
    else: bot.cwpause = True
    bot.refr["pause"] = bot.pause
    await close_admin()
    await ctx.reply(f"Set `pause` to: {bot.pause}")

@bot.command()
@commands.is_owner()
async def cwpause(ctx):
    if bot.cwpause: bot.cwpause = False
    else: bot.cwpause = True
    await ctx.reply(f"Set `cwpause` to: {bot.cwpause}")
    bot.refr["cwpause"] = bot.cwpause
    await close_admin()

@bot.command()
@commands.is_owner()
async def cwtime(ctx, string1, string2):
    secs = await conv_rem(string1)
    secs2 = await conv_rem(string2)
    bot.refr["cwtime_s"] = time.time() + secs
    bot.refr["cwtime_e"] = time.time() + secs2
    await close_admin()
    await ctx.message.add_reaction(economysuccess)

class BotCalculator(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.expr = ""
        self.embed = discord.Embed(description=f"```\n{0}\n```ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                                   color=3092790)

    def updatembed(self):
        if self.expr == "": self.expr = "\u200b"
        self.embed = discord.Embed(description=f"```\n{self.expr}\n```ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                              color=3092790)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1")
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2")
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3")
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="x")
    async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "*"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="←")
    async def backspace(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = self.expr[:-1]
        if len(self.expr) == 0: self.expr = ""
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4")
    async def four(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5")
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6")
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="÷")
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "/"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="Clear")
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7")
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8")
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9")
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="+")
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="=")
    async def equals(self, button: discord.ui.Button, interaction: discord.Interaction):
        expression = self.expr
        for i in range(10):
            expression = expression.replace(f"{i}(", f"{i}*(")
        expression = expression.replace("\u200b", "").replace("^", "**").replace("²", "**2").replace("³", "**3")
        print(expression)
        try:
            calculated = numexpr.evaluate(expression).item()
            self.expr = str(calculated)
        except:
            calculated = "Invalid Expression"
            self.expr = ""

        await interaction.response.edit_message(embed=discord.Embed(description=f"```\n{calculated}\n```ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                              color=3092790))

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="00")
    async def dzero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "00"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0")
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".")
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="–")
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Exit")
    async def exit(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=self.embed, view=self)
        self.stop()

    @discord.ui.button(style=discord.ButtonStyle.green, label="(")
    async def lbracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "("
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label=")")
    async def rbracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += ")"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="x²")
    async def square(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "²"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="x³")
    async def cube(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "³"
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.green, label="√x")
    async def sqrt(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "sqrt("
        self.updatembed()
        await interaction.response.edit_message(embed=self.embed)

@bot.command(aliases=["c", "calc", "ans"])
async def calculator(ctx, *, expression=None):
    if expression is not None:
        await ctx.message.add_reaction(loading)
        try:
            for i in range(10):
                expression = expression.replace(f"{i}(", f"{i}*(")
            expression = expression.replace("^", "**")
            calculated = numexpr.evaluate(expression).item()
            if len(str(calculated)) > 1980:
                raise ValueError("Too big output to display")
            await ctx.reply(content=f'```py\n{calculated}```')
            await ctx.message.clear_reaction(loading)
        except Exception as ex:
            await ctx.reply("Invalid Expression!")
            await ctx.message.clear_reaction(loading)
    else:
        embed = discord.Embed(description="```\n0\n```ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                              color=3092790)
        await ctx.send(embed=embed, view=BotCalculator())

@bot.command()
@commands.is_owner()
async def disable(ctx, cmd, *, reason=None):
    if reason is None: reason = "No reason provided"
    bot.refr["dcmds"][cmd] = reason
    await ctx.message.add_reaction(economysuccess)
    await close_admin()

@bot.command()
@commands.check(general)
async def say(ctx, *, sentence):
    if ctx.author.id not in devs + staff: return
    chl = sentence.split(" ")[0]
    chlmodified = False
    testchl = chl.replace("<#", "").replace(">", "")
    if len(testchl) == len("839080243485736970"):
        try:
            chl = int(testchl)
            saycmd[str(ctx.author.id)] = chl
            chlmodified = True
        except Exception as e:
            pass
    chnid = saycmd.get(str(ctx.author.id))
    if chnid is None:
        return await ctx.reply("No last used channel found! Use `v.sayhelp` for usage")
    chn = bot.get_channel(chnid)
    try:
        if chlmodified:
            sentence_new = " ".join(sentence.split(" ")[1:])
            await chn.send(sentence_new)
        else:
            await chn.send(sentence)
    except:
        ctx.reply("An error occured. Make sure I have sufficient permission in the channel to talk")

@bot.command(aliases=["suggestion", "sug"])
@commands.check(general)
async def suggest(ctx):
    return await ctx.reply("Use `v.post` to post suggestion!")

@bot.command()
@commands.check(general)
async def sayhelp(ctx):
    if ctx.author.id not in devs+staff: return
    msg = "You need to use it like this: `v.say #channel message` for the **first time**. After that, " \
          "whenever you use `v.say`, it will automatically send in the last used channel.\n\n" \
          "To update the channel, use `v.say #channel message` again."
    embed = discord.Embed(title="Say Help",
                          description=msg,
                          colour=localembed)
    await ctx.send(embed=embed)
    
@bot.command()
@commands.check(general)
async def statusw(ctx, *, newst):
    if ctx.author.id not in staff: return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=newst))

@bot.command()
@commands.check(general)
async def statusl(ctx, *, newst):
    if ctx.author.id not in staff: return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=newst))

@bot.command()
@commands.check(general)
async def statusp(ctx, *, newst):
    if ctx.author.id not in staff: return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=newst))

@bot.command(aliases=["soc"])
@commands.check(general)
async def socials(ctx, platform=None, action=None):
    if ctx.author.id not in staff: return
    if platform is None:
        embed = discord.Embed(title="VNTA Social Manager",
                              description="Here are the commands for management:",
                              color=localembed)
        embed.add_field(name=f"{youtube} `v.soc yt`", value="Manage YouTube", inline=False)
        embed.add_field(name=f"{twitch} `v.soc twitch`", value="Manage Twitch", inline=False)
        embed.add_field(name=f"{twitter} `v.soc twitter`", value="Manage Twitter", inline=False)
        return await ctx.send(embed=embed)
    if platform.lower() == "yt":
        await yt_manage(ctx, action)
    elif platform.lower() == "twitch":
        await twitch_manage(ctx, action)
    elif platform.lower() == "twitter":
        await twitter_manage(ctx, action)

async def yt_manage(ctx, action=None):
    if action is None:
        embed = discord.Embed(title="<:YouTube:865575628710608916> YouTube",
                              description="Here are the actions you can perform:",
                              color=localembed)
        embed.add_field(name="`channel`", value="View or change the channel where you want to send notification", inline=False)
        embed.add_field(name="`subs`", value="Check the people whom you have subscribed", inline=False)
        embed.add_field(name="`add`", value="Add a subscription", inline=False)
        embed.add_field(name="`rem`", value="Remove a subscription", inline=False)
        embed.add_field(name="`msg`", value="View or change the message the bot sends", inline=False)
        embed.add_field(name="`role`", value="View or change the role which is pinged", inline=False)
        embed.set_footer(text="Type 'v.socials yt <action>' to view/edit it")
        return await ctx.send(embed=embed)
    ytdata = bot.refr.setdefault("social_yt", {})
    action = action.lower()
    def rcheck(reaction, user_):
        return user_ == ctx.author

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    if action == "channel":
        a = ytdata.setdefault("channel", 0)
        if a == 0: chl = "Not set"
        else: chl = bot.get_channel(a).mention
        embed = discord.Embed(title="Channel", description=f"> {chl}\n"
                                                           f"\n"
                                                           f"To change the channel, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new channel (DO NOT MENTION THE CHANNEL)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = bot.get_channel(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        ytdata["channel"] = newchl.id
        await chlid.add_reaction(economysuccess)
    elif action == "subs":
        subs = ytdata.get("subs", [])
        subs_string = "\n".join(["> https://www.youtube.com/channel/"+x for x in subs])
        if subs_string == "": subs_string = "> No channels subscribed"
        embed = discord.Embed(title="Your Subscriptions",
                              description=subs_string, color=localembed)
        embed.set_footer(text="To add: 'v.socials yt add'\n"
                              "To remove: 'v.socials yt rem'")
        await ctx.send(embed=embed)
    elif action == "add":
        await ctx.reply("Enter the channel URL to add. Prefer regular URL over vanity URL as they are more reliable")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://www.youtube.com/channel/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://www.youtube.com/channel/", "")
        old = ytdata.get("subs", [])
        if finalurl in old:
            return await msg.reply("URL already subscribed!")
        old.append(finalurl)
        ytdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "rem":
        await ctx.reply("Enter the channel URL to remove")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://www.youtube.com/channel/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://www.youtube.com/channel/", "")
        old = ytdata.get("subs", [])
        if finalurl not in old:
            return await msg.reply("URL isn't subscribed!")
        old.remove(finalurl)
        ytdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "msg":
        oldmsg = ytdata.setdefault("msg", "{role} **{name} just uploaded a video! Check it out: {link}**")
        embed = discord.Embed(title="Message", description=f"`{oldmsg}`\n\n"
                                                           f"Variables:\n"
                                                           "`{role}`- Role to ping\n"
                                                           "`{name}`- Name of the channel\n"
                                                           "`{link}`- Link of the video",
                              color=localembed)
        embed.set_footer(text="To change the message, react below")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Enter the new message. You can only use the variables defined above.\n"
                       "Do **not** remove the brackets `{}` from the variables")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        ytdata["msg"] = chlid.content
        await chlid.add_reaction(economysuccess)
    elif action == "role":
        a = ytdata.setdefault("role", 0)
        if a == 0:
            chl = "Not set"
        else:
            chl = ctx.guild.get_role(a).mention
        embed = discord.Embed(title="Role", description=f"> {chl}\n"
                                                           f"\n"
                                                           f"To change the role, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new role (DO NOT MENTION THE ROLE)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = ctx.guild.get_role(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        ytdata["role"] = newchl.id
        await chlid.add_reaction(economysuccess)
    else: return
    bot.refr["social_yt"] = ytdata
    await close_admin()

async def twitch_manage(ctx, action=None):
    if action is None:
        embed = discord.Embed(title="<:Twitch:865575682208825355> Twitch",
                              description="Here are the actions you can perform:",
                              color=localembed)
        embed.add_field(name="`channel`", value="View or change the channel where you want to send notification",
                        inline=False)
        embed.add_field(name="`subs`", value="Check the people whom you have subscribed", inline=False)
        embed.add_field(name="`add`", value="Add a subscription", inline=False)
        embed.add_field(name="`rem`", value="Remove a subscription", inline=False)
        embed.add_field(name="`msg`", value="View or change the message the bot sends", inline=False)
        embed.add_field(name="`role`", value="View or change the role which is pinged", inline=False)
        embed.set_footer(text="Type 'v.socials twitch <action>' to view/edit it")
        return await ctx.send(embed=embed)
    twitchdata = bot.refr.setdefault("social_twitch", {})
    action = action.lower()

    def rcheck(reaction, user_):
        return user_ == ctx.author

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    if action == "channel":
        a = twitchdata.setdefault("channel", 0)
        if a == 0:
            chl = "Not set"
        else:
            chl = bot.get_channel(a).mention
        embed = discord.Embed(title="Channel", description=f"> {chl}\n"
                                                           f"\n"
                                                           f"To change the channel, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new channel (DO NOT MENTION THE CHANNEL)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = bot.get_channel(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        twitchdata["channel"] = newchl.id
        await chlid.add_reaction(economysuccess)
    elif action == "subs":
        subs = twitchdata.get("subs", [])
        subs_string = "\n".join(["> https://www.twitch.tv/" + x for x in subs])
        if subs_string == "": subs_string = "> No channels subscribed"
        embed = discord.Embed(title="Your Subscriptions",
                              description=subs_string, color=localembed)
        embed.set_footer(text="To add: 'v.socials twitch add'\n"
                              "To remove: 'v.socials twitch rem'")
        await ctx.send(embed=embed)
    elif action == "add":
        await ctx.reply("Enter the channel URL to add.")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://www.twitch.tv/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://www.twitch.tv/", "")
        old = twitchdata.get("subs", [])
        if finalurl in old:
            return await msg.reply("URL already subscribed!")
        old.append(finalurl)
        twitchdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "rem":
        await ctx.reply("Enter the channel URL to remove")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://www.twitch.tv/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://www.twitch.tv/", "")
        old = twitchdata.get("subs", [])
        if finalurl not in old:
            return await msg.reply("URL isn't subscribed!")
        old.remove(finalurl)
        twitchdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "msg":
        oldmsg = twitchdata.setdefault("msg", "{role} **{name} is live! {title} Join him: {link}**")
        embed = discord.Embed(title="Message", description=f"`{oldmsg}`\n\n"
                                                           f"Variables:\n"
                                                           "`{role}`- Role to ping\n"
                                                           "`{name}`- Name of the channel\n"
                                                           "`{link}`- Link of the stream\n"
                                                           "`{title}` - Title of the stream",
                              color=localembed)
        embed.set_footer(text="To change the message, react below")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Enter the new message. You can only use the variables defined above.\n"
                       "Do **not** remove the brackets `{}` from the variables")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        twitchdata["msg"] = chlid.content
        await chlid.add_reaction(economysuccess)
    elif action == "role":
        a = twitchdata.setdefault("role", 0)
        if a == 0:
            chl = "Not set"
        else:
            chl = ctx.guild.get_role(a).mention
        embed = discord.Embed(title="Role", description=f"> {chl}\n"
                                                        f"\n"
                                                        f"To change the role, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new role (DO NOT MENTION THE ROLE)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = ctx.guild.get_role(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        twitchdata["role"] = newchl.id
        await chlid.add_reaction(economysuccess)
    else:
        return
    bot.refr["social_twitch"] = twitchdata
    await close_admin()

async def twitter_manage(ctx, action=None):
    if action is None:
        embed = discord.Embed(title="<:Twitter:866566539581587456> Twitter",
                              description="Here are the actions you can perform:",
                              color=localembed)
        embed.add_field(name="`channel`", value="View or change the channel where you want to send notification",
                        inline=False)
        embed.add_field(name="`subs`", value="Check the people whom you have subscribed", inline=False)
        embed.add_field(name="`add`", value="Add a subscription", inline=False)
        embed.add_field(name="`rem`", value="Remove a subscription", inline=False)
        embed.add_field(name="`msg`", value="View or change the message the bot sends", inline=False)
        embed.add_field(name="`role`", value="View or change the role which is pinged", inline=False)
        embed.set_footer(text="Type 'v.socials twitter <action>' to view/edit it")
        return await ctx.send(embed=embed)

    twitterdata = bot.refr.setdefault("social_twitter", {})
    action = action.lower()

    def rcheck(reaction, user_):
        return user_ == ctx.author

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    if action == "channel":
        a = twitterdata.setdefault("channel", 0)
        if a == 0:
            chl = "Not set"
        else:
            chl = bot.get_channel(a).mention
        embed = discord.Embed(title="Channel", description=f"> {chl}\n"
                                                           f"\n"
                                                           f"To change the channel, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new channel (DO NOT MENTION THE CHANNEL)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = bot.get_channel(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        twitterdata["channel"] = newchl.id
        await chlid.add_reaction(economysuccess)
    elif action == "subs":
        subs = twitterdata.get("subs", {})
        subs_string = "\n".join(["> https://www.twitter.com/" + x for x in subs])
        if subs_string == "": subs_string = "> No channels subscribed"
        embed = discord.Embed(title="Your Subscriptions",
                              description=subs_string, color=localembed)
        embed.set_footer(text="To add: 'v.socials twitter add'\n"
                              "To remove: 'v.socials twitter rem'")
        await ctx.send(embed=embed)
    elif action == "add":
        header = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
        await ctx.reply("Enter the channel URL to add.")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://twitter.com/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://twitter.com/", "")
        old = twitterdata.get("subs", {})
        if finalurl in old.keys():
            return await msg.reply("URL already subscribed!")
        uri = f"https://api.twitter.com/2/users/by/username/{finalurl}"
        a = requests.get(uri, headers=header)
        data = json.loads(a.text)
        data = data["data"]
        old[finalurl] = data["id"]
        twitterdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "rem":
        await ctx.reply("Enter the channel URL to remove")
        msg = await bot.wait_for("message", timeout=60, check=check)
        msgc = msg.content
        if "https://twitter.com/" not in msgc:
            return await msg.reply("Invalid URL")
        finalurl = msgc.replace("https://twitter.com/", "")
        old = twitterdata.get("subs", {})
        if finalurl not in old:
            return await msg.reply("URL isn't subscribed!")
        old.pop(finalurl)
        twitterdata["subs"] = old
        await msg.add_reaction(economysuccess)
    elif action == "msg":
        oldmsg = twitterdata.setdefault("msg", "{role} **{name}** just posted a tweet! Check it out here: {link}")
        embed = discord.Embed(title="Message", description=f"`{oldmsg}`\n\n"
                                                           f"Variables:\n"
                                                           "`{role}`- Role to ping\n"
                                                           "`{name}`- Name of the handle\n"
                                                           "`{link}`- Link of the tweet",
                              color=localembed)
        embed.set_footer(text="To change the message, react below")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Enter the new message. You can only use the variables defined above.\n"
                       "Do **not** remove the brackets `{}` from the variables")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        twitterdata["msg"] = chlid.content
        await chlid.add_reaction(economysuccess)
    elif action == "role":
        a = twitterdata.setdefault("role", 0)
        if a == 0:
            chl = "Not set"
        else:
            chl = ctx.guild.get_role(a).mention
        embed = discord.Embed(title="Role", description=f"> {chl}\n"
                                                        f"\n"
                                                        f"To change the role, react with 🇨",
                              color=localembed)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🇨")

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if str(reaction.emoji) != "🇨": return
        await ctx.send("Send the ID of the new role (DO NOT MENTION THE ROLE)")

        chlid = await bot.wait_for("message", timeout=60, check=check)
        try:
            newchl = int(chlid.content)
            newchl = ctx.guild.get_role(newchl)
            if newchl is None: raise ValueError
        except:
            return await chlid.reply("Invalid ID")
        twitterdata["role"] = newchl.id
        await chlid.add_reaction(economysuccess)
    else:
        return
    bot.refr["social_twitter"] = twitterdata
    await close_admin()

@bot.command()
@commands.is_owner()
async def enable(ctx, cmd):
    bot.refr["dcmds"].pop(cmd)
    await ctx.message.add_reaction(economysuccess)
    await close_admin()

@bot.command()
@commands.is_owner()
async def usage(ctx, state=None):
    if state is None:
        embed = discord.Embed(title="🔴 Updating Live",
                             description="Running Tests...",
                             color=localembed)
        bot.usagemsg = await ctx.send(embed=embed)
    else: bot.usage_ = False
    while True:
        if not bot.usage_:
            embed = discord.Embed(title="⚪ Stopped",
                                  color=localembed)
            await bot.usagemsg.edit(embed=embed)
            break
        mempercent = psutil.virtual_memory().percent
        cpupercent = psutil.cpu_percent()
        netusage = get_net_usage()
        x = PrettyTable()
        x.field_names = ["Type", "Usage"]
        x.add_row(["RAM", f"{mempercent}%"])
        x.add_row(["CPU", f"{cpupercent}%"])
        x.add_row(["Network", f"{int(float(netusage))} KB"])
        x.title = "Usage Stats"
        embed = discord.Embed(title="🔴 Updating Live",
                              description=f"```\n{x}```",
                              color=localembed)
        await bot.usagemsg.edit(embed = embed)
        await asyncio.sleep(1.1)

@bot.command()
@commands.check(general)
async def mute(ctx, mem:discord.Member):
    bot.refr["disregarded"].append(mem.id)
    embed = discord.Embed(title=f'{economyerror} Warning!',
                          description=f'{mem.mention} has been disregarded!',
                          color=error_embed)
    await ctx.send(embed=embed)

@bot.command()
@commands.check(general)
async def unmute(ctx, mem:discord.Member):
    bot.refr["disregarded"].remove(mem.id)
    await ctx.message.add_reaction(economysuccess)

@bot.command()
async def chatbot(ctx, webhook: str):
    if ctx.author.id not in staff:
        return
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook, session=session, bot_token=bot.http.token)
        webhook = await bot.fetch_webhook(webhook.id)
        bot.refr["cbChl"] = webhook.channel.id
        bot.refr["cbWeb"] = webhook.id

    await ctx.reply(f"Chatbot setup @ {webhook.channel.mention} via `{webhook.id}:{webhook.type}`")
    await close_admin()

def get_net_usage():
    old_value = 0
    new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    diff = new_value - old_value
    old_value = new_value
    return "{:.3f}".format(diff/8000)

async def load_data():
    chl = bot.get_channel(854692793276170280)
    msgs = [x async for x in chl.history(limit=1)]
    bot.refr = json.loads(requests.get(msgs[0].attachments[0]).text)
    bot.cwpause = bot.refr["cwpause"]
    bot.pause = bot.refr["pause"]

    chl = bot.get_channel(854721559359913994)
    msgs = [x async for x in chl.history(limit=1)]
    bot.links.update(json.loads(requests.get(msgs[0].attachments[0]).text))

    chl = bot.get_channel(856070919033978932)
    msgs = [x async for x in chl.history(limit=1)]
    bot.userdata = json.loads(requests.get(msgs[0].attachments[0]).text)

    chl = bot.get_channel(854698116255318057)
    msgs = [x async for x in chl.history(limit=1)]
    bot.bgdata = json.loads(requests.get(msgs[0].attachments[0]).text)

async def one_ready():
    global staff
    print("Connected")
    await bot.wait_until_ready()
    staff = [x.id for x in bot.get_guild(719946380285837322).get_role(813439914862968842).members]
    await load_data()
    await load_peeps()
    print("Ready")
    vnta = bot.get_guild(719946380285837322)
    bot.starboards = bot.get_channel(874717466134208612)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{vnta.member_count} peeps"))
    bot.dev = bot.get_user(771601176155783198)
    bot.linkinglogs = bot.get_channel(861463678179999784)
    if not bot.pause or not bot.beta:
        if not bot.cwpause: auto_update.start()
    if not bot.beta:
        handle_rems.start()
        yt_socials_check.start()
        twitch_socials_check.start()
        twitter_socials_check.start()
        fotd_check.start()

@bot.command(aliases=["addemoji"])
@commands.has_permissions(manage_emojis=True)
async def steal(ctx:Context, name:str, emoji:Union[discord.Emoji, str]=None):
    url = ""
    if isinstance(emoji, discord.Emoji):
        url = emoji.url
    elif isinstance(emoji, str):
        url = emoji
    elif emoji is None and len(ctx.message.attachments) != 0:
        url = ctx.message.attachments[0].url
    else:
        await ctx.send("Incorrect Syntax! Use `v.steal <name> [url or emoji or file-attachment]`")

    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            a = r.content
            name = name.replace(" ", "_")
            if len(name) < 2:
                return await ctx.reply("Name should be minimum 2 characters long")
            newemoji = await ctx.guild.create_custom_emoji(name=name, image=a)
            await ctx.send(f"Added emoji successfully!\nEmoji: {newemoji}\nName: {newemoji.name}\nCode: `:{newemoji.name}:{newemoji.id}:`")
        else:
            await ctx.reply("Invalid URL")
    except Exception as e:
        await ctx.send(f"An error occured: {e}")

@bot.command()
async def post(ctx):
    view = Post(ctx)
    a = await ctx.send("Select the type:", view=view)
    view.msg = a

class Post(discord.ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.ctx = ctx
        self.msg = None

    @discord.ui.button(label="Suggestion", emoji="👤", style=discord.ButtonStyle.green)
    async def suggestion(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.defer()
        ctx = self.ctx
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await interaction.response.send_message("Enter your suggestion", ephemeral=True)
        try:
            msg = await bot.wait_for("message", timeout=180, check=check)
            sug = msg.content
            stfchl = bot.get_channel(813447381752348723)
            embed = discord.Embed(title="Suggestion Approval",
                                  description=sug,
                                  color=localembed)
            embed.set_author(name=ctx.author, icon_url=ctx.author.default_avatar.url)
            em = await stfchl.send(embed=embed)
            bot.refr["review"]["suggest"][str(em.id)] = (ctx.author.id, sug)
            bot.refr["types"][str(em.id)] = "suggest"
            await msg.delete()
            await ctx.send(
                "Your suggestion is sent to staff for approval."
                " It will show in <#861555361264697355> once its approved!")
            await em.add_reaction(economysuccess)
            await em.add_reaction(economyerror)

        except:
            pass

    @discord.ui.button(label="Settings", emoji="⚙️", style=discord.ButtonStyle.grey)
    async def settings(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.defer()
        ctx = self.ctx
        def check(msg):
            return msg.author == ctx.author and len(msg.attachments) != 0

        await interaction.response.send_message("Upload the `.txt` file", ephemeral=True)
        try:
            msg = await bot.wait_for("message", timeout=180, check=check)
            file = msg.attachments[0].url
            async with aiohttp.ClientSession() as session:
                async with session.get(file) as r:
                    text = await r.text()
                    with open(f"settings.txt", "w", encoding='utf8') as f:
                        f.write(text)
                    file = discord.File("settings.txt")
                    a = await bot.get_channel(865587676999843840).send(file=file)
                    file = a.attachments[0].url
            await msg.delete()
            await ctx.send(
                "Your settings are sent to staff for approval. It will show in <#882312116797861899> once they are approved!")
            embed = discord.Embed(title="Settings Approval",
                                  description=file,
                                  color=localembed)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.default_avatar.url)
            a = await bot.get_channel(813447381752348723).send(embed=embed)
            await a.add_reaction(economysuccess)
            await a.add_reaction(economyerror)
            bot.refr["review"]["settings"][str(a.id)] = [ctx.author.id, file]
            bot.refr["types"][str(a.id)] = "settings"
        except asyncio.TimeoutError:
            pass

    @discord.ui.button(label="CSS", emoji="🗒️", style=discord.ButtonStyle.red)
    async def css(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.defer()
        ctx = self.ctx

        def check(msg):
            return msg.author == ctx.author and len(msg.attachments) != 0

        await interaction.response.send_message("Upload the `.css` file", ephemeral=True)
        try:
            msg = await bot.wait_for("message", timeout=180, check=check)
            file = msg.attachments[0].url
            async with aiohttp.ClientSession() as session:
                async with session.get(file) as r:
                    text = await r.text()
                    with open(f"main_custom.css", "w", encoding='utf8') as f:
                        f.write(text)
                    file = discord.File("main_custom.css")
                    a = await bot.get_channel(865587676999843840).send(file=file)
                    file = a.attachments[0].url
            await msg.delete()
            await ctx.send(
                "Your css is sent to staff for approval. It will show in <#882312235416965120> once it is approved!")
            embed = discord.Embed(title="CSS Approval",
                                  description=file,
                                  color=localembed)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.default_avatar.url)
            a = await bot.get_channel(813447381752348723).send(embed=embed)
            await a.add_reaction(economysuccess)
            await a.add_reaction(economyerror)
            bot.refr["review"]["css"][str(a.id)] = [ctx.author.id, file]
            bot.refr["types"][str(a.id)] = "css"
        except asyncio.TimeoutError:
            pass

    @discord.ui.button(label="Scope", emoji="🔭", style=discord.ButtonStyle.blurple)
    async def scope(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.defer()
        ctx = self.ctx

        def check(msg):
            return msg.author == ctx.author and len(msg.attachments) != 0

        await interaction.response.send_message("Upload the `.png` file (DO NOT SEND THE LINK)", ephemeral=True)
        try:
            msg = await bot.wait_for("message", timeout=180, check=check)
            file = msg.attachments[0].url
            await msg.delete()
            await ctx.send(
                "Your scope is sent to staff for approval. It will show in <#882312052432068689> once it is approved!")
            embed = discord.Embed(title="Scope Approval",
                                  color=localembed)
            embed.set_image(url=file)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.default_avatar.url)
            a = await bot.get_channel(813447381752348723).send(embed=embed)
            await a.add_reaction(economysuccess)
            await a.add_reaction(economyerror)
            bot.refr["review"]["scopes"][str(a.id)] = [ctx.author.id, file]
            bot.refr["types"][str(a.id)] = "scope"
        except asyncio.TimeoutError:
            pass

async def chatbotReply(message: discord.Message):
    content = message.content
    apiKey = bot.refr.get("apiKey")
    webhook = await bot.fetch_webhook(bot.refr["cbWeb"])
    if bot.session is None:
        bot.session = aiohttp.ClientSession()
    reply = await bot.session.get(f"https://some-random-api.ml/chatbot?message={content}&key={apiKey}")
    reply = await reply.json()
    if reply.get("error") is not None:
        return
    await webhook.send(f"> {content}\n"
                       f"{reply['response']}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    def get_ops(text):
        if text == "": return {}
        text = text.replace("\n\n", "\n> ")
        ops = text.split("\n> ")
        i = 0
        sugs = {}
        while i < len(ops):
            user = int(ops[i].replace("<@", "").replace(">", ""))
            sug = ops[i+1]
            sugs[user] = sug
            i += 2
        return sugs

    if message.channel.id == bot.refr.get("cbChl", 0) and message.reference is None:
        await chatbotReply(message)

    if bot.beta:
        if message.guild is None: return
        if message.guild.id != 826824650713595964: return
    else:
        if message.channel.id == 864755738609057822:
            data = "{" + message.content + "}"
            data = dict(eval(data))
            old = bot.refr.setdefault("con", {})
            for k, v in data.items():
                old[str(k)] = v
            bot.refr["con"] = old
            await close_admin()
        if (message.channel.id == 861555361264697355) and (message.reference is not None):
            reply = message.reference.message_id
            msg = await message.channel.fetch_message(reply)
            embed = msg.embeds[0]
            oldval = ""
            for index, i in enumerate(embed.fields):
                if i.name == "Staff Opinions:":
                    oldval = i.value
                    embed.remove_field(index)
                    break
            if oldval == "\u200b": oldval = ""
            ops = get_ops(oldval)
            ops[message.author.id] = message.content
            oldval = ""
            for k, v in ops.items():
                print(k, v)
                oldval += f"<@{k}>\n> {v}\n\n"
            embed.add_field(name="Staff Opinions:", value=oldval)
            await msg.edit(embed=embed)
            await message.delete(delay=2)
        if message.type in [discord.MessageType.premium_guild_subscription, discord.MessageType.premium_guild_tier_1,
                            discord.MessageType.premium_guild_tier_2, discord.MessageType.premium_guild_tier_3]:
            user = message.author
            emoji = "<a:Boost_Spin:883010481437155368>"
            perks = """__**Single Booster Perks:**__
        
                    <a:Boost_Spin:883010481437155368> 3x Claim Time on all Giveaways!
                    <a:Boost_Spin:883010481437155368> Bypass all requirements on Giveaways!
                    <a:Boost_Spin:883010481437155368> Custom Emote + Name (No NSFW)!
                    <a:Boost_Spin:883010481437155368> Custom Role!
                    <a:Boost_Spin:883010481437155368> 5x Extra Entries on all Giveaways! 
                    <a:Boost_Spin:883010481437155368> Hoisted role above all members!
                    <a:Boost_Spin:883010481437155368> Extra permissions in Text & Voice channels!
                    <a:Boost_Spin:883010481437155368> 15% Discount on all ads you purchase!
        
                    __**Double Booster Perks:**__
        
                    <a:boost_evolve:829395858961334353> 10x Extra Entries!
                    <a:boost_evolve:829395858961334353> Unlimited Claim Time on Giveaways!
                    <a:boost_evolve:829395858961334353> Reaction with your emote!
                    <a:boost_evolve:829395858961334353> Respect from all Staff!
                    <a:boost_evolve:829395858961334353> An extra 20% off ads, totalling at a 35% discount!
        
                    **Create a ticket in <#813510158264565780> to claim your perks and thank you for boosting!**"""
            embed = discord.Embed(color=localembed,
                                  description=f"{emoji} Thank you for boosting {user.mention}! {emoji}\n" \
                                              f"We now have {bot.get_guild(719946380285837322).premium_subscription_count} boosts! **Remember to claim your perks:**\n\n"
                                              f"{perks}")
            if user.avatar is not None:
                url = user.avatar.url
            else:
                url = user.default_avatar.url
            embed.set_author(name=str(user), icon_url=url)
            embed.set_footer(text="#vantalizing")
            embed.timestamp = datetime.datetime.utcnow()
            await bot.get_channel(813435497442967562).send(content=f"{user.mention}", embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == 853971223682482226: return
    if str(payload.emoji) == "⭐":
        return await starboard(payload)
    if str(payload.emoji) == "✨" and payload.user_id in staff:
        msg = await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.add_reaction("⭐")
        await msg.clear_reaction("✨")
        return await starboard(payload, force=True)
    if payload.message_id in bot.pendings and str(payload.emoji) in [economyerror, economysuccess]:
        chan = bot.get_channel(payload.channel_id)
        userd = bot.pendings[payload.message_id]
        user = userd[0]
        if payload.user_id != userd[0]: return
        user = bot.get_user(user)
        if str(payload.emoji) == "❌":
            await chan.send(f"{user.mention} Link request was cancelled..")
        else:
            was_success = False
            for i in range(5):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://kr.vercel.app/api/profile?username={userd[1]}") as data:
                        if data.status == 200:
                            was_success = True
                            datatext = await data.text()
                            break
            if not was_success:
                embed = discord.Embed(title=f"{economyerror} Error",
                                      description="API didnt respond in time",
                                      color=error_embed)
                embed.set_footer(text="Please try again later")
                return await chan.send(f"{user.mention}", embed=embed)

            userdata = json.loads(datatext)
            oldflag = userdata["data"]["stats"].get("flg", "a")
            if oldflag != userd[2]:
                return await chan.send(f"{user.mention} The flag change wasn't detected. Make sure to stick to the end of the match\n"
                                       f"**Note: If you are linked with GameBot, ask a staff to forcelink you**")
            t = bot.links.get(str(user.id), {"main":userdata['data']['username'], "all":[]})
            t["all"] = list(set(t["all"]))
            t["all"].append(userdata['data']['username'])
            bot.links[str(user.id)] = t
            await update_links()
            await chan.send(f"{user.mention} {economysuccess} You are successfully linked with `{userdata['data']['username']}`!")
            await linklog(ign=userdata['data']['username'], user=user, t="l")
        bot.pendings.pop(payload.message_id)
    if payload.channel_id == 813447381752348723 and str(payload.emoji) in [economyerror, economysuccess]:
        rev_type = bot.refr["types"].get(str(payload.message_id))
        if rev_type == "suggest":
            await suggest_approval(payload)
        elif rev_type == "settings":
            await settings_approval(payload)
        elif rev_type == "css":
            await css_approval(payload)
        elif rev_type == "scope":
            await scope_approval(payload)

async def suggest_approval(payload: discord.RawReactionActionEvent):
    chan = bot.get_channel(payload.channel_id)
    userd = bot.refr["review"]["suggest"].get(str(payload.message_id))
    mod = bot.get_user(payload.user_id)
    if userd is None: return
    user = userd[0]
    user = bot.get_user(user)
    if str(payload.emoji) == "❌":
        await user.send(f"{economyerror} Your suggestion: `{userd[1]}` was rejected by `{mod}`")
    else:
        await user.send(f"{economysuccess} Your suggestion: `{userd[1]}` was accepted by `{mod}`")
        sugchl = bot.get_channel(861555361264697355)
        embed = discord.Embed(description=userd[1],
                              color=localembed)
        embed.add_field(name="Staff Opinions:", value="\u200b")
        if user.avatar is not None:
            url = user.avatar.url
        else:
            url = user.default_avatar.url
        embed.set_author(name=f"By: {user}", icon_url=url)
        embed.set_footer(text="#vantalizing")
        embed.timestamp = datetime.datetime.utcnow()
        em = await sugchl.send(embed=embed)
        await em.add_reaction("👍")
        await em.add_reaction("👎")
    bot.refr["review"]["suggest"].pop(str(payload.message_id))

async def settings_approval(payload: discord.RawReactionActionEvent):
    chan = bot.get_channel(payload.channel_id)
    userd = bot.refr["review"]["settings"].get(str(payload.message_id))
    mod = bot.get_user(payload.user_id)
    if userd is None: return
    user = userd[0]
    user = bot.get_user(user)
    if str(payload.emoji) == "❌":
        await user.send(f"{economyerror} Your settings: `{userd[1]}` was rejected by `{mod}`")
    else:
        await user.send(f"{economysuccess} Your settings: `{userd[1]}` was accepted by `{mod}` and"
                        f" are added to <#882312116797861899>")
        chl = bot.get_channel(882312116797861899)
        async with aiohttp.ClientSession() as session:
            async with session.get(userd[1]) as r:
                text = await r.text()
                with open(f"settings.txt", "w", encoding='utf8') as f:
                    f.write(text)
        file = discord.File("settings.txt")
        em = await chl.send(f"Settings by: {user.mention}\n"
                            f"React with 👍 or 👎 to rate it",
                            file=file)
        await em.add_reaction("👍")
        await em.add_reaction("👎")
        bot.refr["added"]["settings"].append(em.id)
    bot.refr["review"]["settings"].pop(str(payload.message_id))

async def css_approval(payload: discord.RawReactionActionEvent):
    chan = bot.get_channel(payload.channel_id)
    userd = bot.refr["review"]["css"].get(str(payload.message_id))
    mod = bot.get_user(payload.user_id)
    if userd is None: return
    user = userd[0]
    user = bot.get_user(user)
    if str(payload.emoji) == "❌":
        await user.send(f"{economyerror} Your css: `{userd[1]}` was rejected by `{mod}`")
    else:
        await user.send(f"{economysuccess} Your css: `{userd[1]}` was accepted by `{mod}` and"
                        f" are added to <#882312235416965120>")
        chl = bot.get_channel(882312235416965120)
        async with aiohttp.ClientSession() as session:
            async with session.get(userd[1]) as r:
                text = await r.text()
                with open(f"main_custom.css", "w", encoding='utf8') as f:
                    f.write(text)
        file = discord.File("main_custom.css")
        em = await chl.send(f"CSS by: {user.mention}\n"
                            f"React with 👍 or 👎 to rate it",
                            file=file)
        await em.add_reaction("👍")
        await em.add_reaction("👎")
        bot.refr["added"]["css"].append(em.id)
    bot.refr["review"]["css"].pop(str(payload.message_id))

async def scope_approval(payload: discord.RawReactionActionEvent):
    chan = bot.get_channel(payload.channel_id)
    userd = bot.refr["review"]["scopes"].get(str(payload.message_id))
    mod = bot.get_user(payload.user_id)
    if userd is None: return
    user = userd[0]
    user = bot.get_user(user)
    if str(payload.emoji) == "❌":
        await user.send(f"{economyerror} Your scope: `{userd[1]}` was rejected by `{mod}`")
    else:
        await user.send(f"{economysuccess} Your scope: `{userd[1]}` was accepted by `{mod}` and"
                        f" are added to <#882312052432068689>")
        chl = bot.get_channel(882312052432068689)
        em = await chl.send(f"Scope by: {user.mention}\n"
                            f"{userd[1]}\n\n"
                            f"React with 👍 or 👎 to rate it")
        await em.add_reaction("👍")
        await em.add_reaction("👎")
        bot.refr["added"]["scopes"].append(em.id)
    bot.refr["review"]["scopes"].pop(str(payload.message_id))

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == 853971223682482226: return
    if str(payload.emoji) == "⭐":
        return await starboard(payload)

@bot.event
async def on_member_update(before, after):
    if before.roles == after.roles: return
    autroles = [y.id for y in after.roles]
    vnta = bot.get_guild(719946380285837322)
    for k, v in order.items():
        if any([x in autroles for x in v]):
            if k not in autroles:
                await after.add_roles(vnta.get_role(k))
        else:
            if k in autroles:
                await after.remove_roles(vnta.get_role(k))

@bot.command()
@commands.is_owner()
async def dividers(ctx):
    vnta = bot.get_guild(719946380285837322)
    i = 1
    for after in vnta.members:
        print(f"Divider for {after} ({i}/{len(vnta.members)})")
        autroles = [y.id for y in after.roles]
        for k, v in order.items():
            if any([x in autroles for x in v]):
                if k not in autroles:
                    print(f"  |- Added {k}")
                    await after.add_roles(vnta.get_role(k))
            else:
                if k in autroles:
                    print(f"  |- Removed {k}")
                    await after.remove_roles(vnta.get_role(k))
        i += 1
        print()

async def starboard(payload:discord.RawReactionActionEvent, force=False):
    msg = await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
    stars_ = msg.reactions
    stars = 0
    for i in stars_:
        if str(i.emoji) == "⭐":
            stars = i.count
            break
    msgdata = bot.refr.setdefault("starboard", {})
    if msgdata.get(str(payload.message_id)) is not None:
        oldmsg = msgdata[str(payload.message_id)]
        msg = await bot.get_guild(payload.guild_id).get_channel(874717466134208612).fetch_message(int(oldmsg))
        await msg.edit(content=f"✨ **{stars}** <#{payload.channel_id}>")

    elif (stars >= 5 and (msgdata.get(str(payload.message_id)) is None)) or force:
        embed = discord.Embed(description=msg.content, color=localembed)
        if msg.author.avatar is not None:
            url = msg.author.avatar.url
        else:
            url = msg.author.default_avatar.url
        embed.set_author(name=msg.author, icon_url=url)
        embed.add_field(name="Orignal", value=f"[Jump!]({msg.jump_url})")
        embed.timestamp = datetime.datetime.utcnow()
        if len(msg.attachments) != 0:
            embed.set_image(url=msg.attachments[0].url)
        msg = await bot.starboards.send(f"✨ **{stars}** <#{payload.channel_id}>", embed=embed)
        msgdata[str(payload.message_id)] = str(msg.id)
        await close_admin()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure): return

    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    print(traceback_text)
    lent = 1970 - len(ctx.message.content)
    await bot.get_channel(873038954163748954).send(f"Command: `{ctx.message.content}`\n"
                                                   f"```py\n{traceback_text[:lent]}```")

@auto_update.error
async def autoerror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: auto_updater\n"
                                                   f"```py\n{traceback_text[:1979]}```")

@yt_socials_check.error
async def yterror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: yt_socials_check\n"
                                                   f"```py\n{traceback_text[:1970]}```")

@twitch_socials_check.error
async def twitcherror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: twitch_socials_check\n"
                                                   f"```py\n{traceback_text[:1970]}```")

@twitter_socials_check.error
async def twittererror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: twitter_socials_check\n"
                                                   f"```py\n{traceback_text[:1970]}```")

@fotd_check.error
async def fotderror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: fotd_check\n"
                                                   f"```py\n{traceback_text[:1979]}```")

@handle_rems.error
async def handleerror(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    if bot.beta: print(traceback_text); return
    await bot.get_channel(873038954163748954).send(f"Task: handle_rems\n"
                                                   f"```py\n{traceback_text[:1979]}```")

bot.loop.create_task(one_ready())
bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")
