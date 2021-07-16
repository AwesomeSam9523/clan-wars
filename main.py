import asyncio, discord, json, sys, random, copy, aiohttp, traceback
import time, datetime, os, threading, requests, psutil, functools, numexpr
from prettytable import PrettyTable
from discord.ext import commands, tasks
from discord.ext.commands import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageSequence, ImageColor
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

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

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Pubstomper", custom_id="pubs_",
                              emoji="<:smg:861873439421235220>")
    async def pubsb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await pubs(interaction)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Clan Wars", custom_id="wars_",
                              emoji="<:bowman:861873349121802251>")
    async def warsb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await wars(interaction)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="Competitive", custom_id="comp_",
                              emoji="<:ak:861873538134573056>")
    async def compb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await comp(interaction)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Content Creation", custom_id="cc_",
                              emoji="<:trooper:861873482576953385>")
    async def ccb(self, button: discord.ui.Button, interaction: discord.Interaction):
        await cc(interaction)

bot = PersistentViewBot()
bot.remove_command("help")
bot.loop.set_debug(True)
bot.loop.slow_callback_duration = 0.3
bot.refr = {}
bot.links = {}
bot.userdata = {}
bot.bgdata = {}
bot.suggestions = {}
bot.cwdata = {}
bot.unsaved = {}
bot.cache = {}
bot.pendings = {}
bot.already = []
bot.vntapeeps = []
bot.excl = [671436261482823763]
bot.dcmds = []
bot.dev = bot.get_user(771601176155783198)
bot.linkinglogs = bot.get_channel(861463678179999784)
bot.interlist = []
bot.uptime = time.time()
bot.reqs = 0
bot.pause = False
bot.cwpause = True
allowdevs = False
if os.path.exists("C:"): bot.beta = True
else: bot.beta = False
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
        "v.suggest":{
            "aliases":["sug", "suggestion"],
            "desc":"Suggest something.",
            "usage":"v.sug <suggestion>"
        }
    },
    "Staff": {
        "category":"Staff",
        "v.cbg":{
            "aliases":["None"],
            "usage":"v.cbg",
            "desc":"Edit clan background"
        },
        "v.forcelink":{
            "aliases":["fl", "forcel", "flink"],
            "usage":"v.forcelink @user <ign>",
            "desc":"Force link a user with an account"
        },
        "e.set_chl": {
            "aliases": ["add_chl"],
            "usage": "e.set_chl <#channel>",
            "desc": "Allows the bot to respond in that channel",
        },
        "v.del_chl": {
            "aliases": ["delete_chl", "rem_chl", "remove_chl"],
            "usage": "e.del_chl <#channel>",
            "desc": "Disallows the bot to respond in that channel",
        },
        "v.list_chl": {
            "aliases": ["show_chl"],
            "usage": "e.list_chl",
            "desc": "Lists all the channels where the bot is allowed to respond",
        },
        "v.reset_chl": {
            "aliases": ["None"],
            "usage": "e.reset_chl",
            "desc": "Clears all the configuration and makes the bot to respond again in **all** the channels",
        }
    }
}

disregarded = []
warn1 = []
warn2 = []
devs = [771601176155783198]
staffchl = [854008993248051230, 813444187566506027]
flags_list = [['Afghanistan', 'af', 0], ['Albania', 'al', 1], ['Algeria', 'dz', 2], ['American Samoa', 'as', 3], ['Andorra', 'ad', 4], ['Angola', 'ao', 5], ['Anguilla', 'ai', 6], ['Antarctica', 'aq', 7], ['Antigua and Barbuda', 'ag', 8], ['Argentina', 'ar', 9], ['Armenia', 'am', 10], ['Aruba', 'aw', 11], ['Australia', 'au', 12], ['Austria', 'at', 13], ['Azerbaijan', 'az', 14], ['Bahamas', 'bs', 15], ['Bahrain', 'bh', 16], ['Bangladesh', 'bd', 17], ['Barbados', 'bb', 18], ['Belarus', 'by', 19], ['Belgium', 'be', 20], ['Belize', 'bz', 21], ['Benin', 'bj', 22], ['Bermuda', 'bm', 23], ['Bhutan', 'bt', 24], ['Bolivia', 'bo', 25], ['Bosnia and Herzegovina', 'ba', 26], ['Botswana', 'bw', 27], ['Brazil', 'br', 28], ['British Indian Ocean Territory', 'io', 29], ['British Virgin Islands', 'vg', 30], ['Brunei', 'bn', 31], ['Bulgaria', 'bg', 32], ['Burkina Faso', 'bf', 33], ['Burundi', 'bi', 34], ['Cambodia', 'kh', 35], ['Cameroon', 'cm', 36], ['Canada', 'ca', 37], ['Cape Verde', 'cv', 38], ['Cayman Islands', 'ky', 39], ['Central African Republic', 'cf', 40], ['Chad', 'td', 41], ['Chile', 'cl', 42], ['China', 'cn', 43], ['Christmas Island', 'cx', 44], ['Cocos Islands', 'cc', 45], ['Colombia', 'co', 46], ['Comoros', 'km', 47], ['Cook Islands', 'ck', 48], ['Costa Rica', 'cr', 49], ['Croatia', 'hr', 50], ['Cuba', 'cu', 51], ['Curacao', 'cw', 52], ['Cyprus', 'cy', 53], ['Czech Republic', 'cz', 54], ['Democratic Republic of the Congo', 'cd', 55], ['Denmark', 'dk', 56], ['Djibouti', 'dj', 57], ['Dominica', 'dm', 58], ['Dominican Republic', 'do', 59], ['East Timor', 'tl', 60], ['Ecuador', 'ec', 61], ['Egypt', 'eg', 62], ['El Salvador', 'sv', 63], ['Equatorial Guinea', 'gq', 64], ['Eritrea', 'er', 65], ['Estonia', 'ee', 66], ['Ethiopia', 'et', 67], ['Falkland Islands', 'fk', 68], ['Faroe Islands', 'fo', 69], ['Fiji', 'fj', 70], ['Finland', 'fi', 71], ['France', 'fr', 72], ['French Polynesia', 'pf', 73], ['Gabon', 'ga', 74], ['Gambia', 'gm', 75], ['Georgia', 'ge', 76], ['Germany', 'de', 77], ['Ghana', 'gh', 78], ['Gibraltar', 'gi', 79], ['Greece', 'gr', 80], ['Greenland', 'gl', 81], ['Grenada', 'gd', 82], ['Guam', 'gu', 83], ['Guatemala', 'gt', 84], ['Guernsey', 'gg', 85], ['Guinea', 'gn', 86], ['Guinea-Bissau', 'gw', 87], ['Guyana', 'gy', 88], ['Haiti', 'ht', 89], ['Honduras', 'hn', 90], ['Hong Kong', 'hk', 91], ['Hungary', 'hu', 92], ['Iceland', 'is', 93], ['India', 'in', 94], ['Indonesia', 'id', 95], ['Iran', 'ir', 96], ['Iraq', 'iq', 97], ['Ireland', 'ie', 98], ['Isle of Man', 'im', 99], ['Israel', 'il', 100], ['Italy', 'it', 101], ['Ivory Coast', 'ci', 102], ['Jamaica', 'jm', 103], ['Japan', 'jp', 104], ['Jersey', 'je', 105], ['Jordan', 'jo', 106], ['Kazakhstan', 'kz', 107], ['Kenya', 'ke', 108], ['Kiribati', 'ki', 109], ['Kosovo', 'xk', 110], ['Kuwait', 'kw', 111], ['Kyrgyzstan', 'kg', 112], ['Laos', 'la', 113], ['Latvia', 'lv', 114], ['Lebanon', 'lb', 115], ['Lesotho', 'ls', 116], ['Liberia', 'lr', 117], ['Libya', 'ly', 118], ['Liechtenstein', 'li', 119], ['Lithuania', 'lt', 120], ['Luxembourg', 'lu', 121], ['Macau', 'mo', 122], ['Macedonia', 'mk', 123], ['Madagascar', 'mg', 124], ['Malawi', 'mw', 125], ['Malaysia', 'my', 126], ['Maldives', 'mv', 127], ['Mali', 'ml', 128], ['Malta', 'mt', 129], ['Marshall Islands', 'mh', 130], ['Mauritania', 'mr', 131], ['Mauritius', 'mu', 132], ['Mayotte', 'yt', 133], ['Mexico', 'mx', 134], ['Micronesia', 'fm', 135], ['Moldova', 'md', 136], ['Monaco', 'mc', 137], ['Mongolia', 'mn', 138], ['Montenegro', 'me', 139], ['Montserrat', 'ms', 140], ['Morocco', 'ma', 141], ['Mozambique', 'mz', 142], ['Myanmar', 'mm', 143], ['Namibia', 'na', 144], ['Nauru', 'nr', 145], ['Nepal', 'np', 146], ['Netherlands', 'nl', 147], ['Netherlands Antilles', 'an', 148], ['New Caledonia', 'nc', 149], ['New Zealand', 'nz', 150], ['Nicaragua', 'ni', 151], ['Niger', 'ne', 152], ['Nigeria', 'ng', 153], ['Niue', 'nu', 154], ['North Korea', 'kp', 155], ['Northern Mariana Islands', 'mp', 156], ['Norway', 'no', 157], ['Oman', 'om', 158], ['Pakistan', 'pk', 159], ['Palau', 'pw', 160], ['Palestine', 'ps', 161], ['Panama', 'pa', 162], ['Papua New Guinea', 'pg', 163], ['Paraguay', 'py', 164], ['Peru', 'pe', 165], ['Philippines', 'ph', 166], ['Pitcairn', 'pn', 167], ['Poland', 'pl', 168], ['Portugal', 'pt', 169], ['Puerto Rico', 'pr', 170], ['Qatar', 'qa', 171], ['Republic of the Congo', 'cg', 172], ['Reunion', 're', 173], ['Romania', 'ro', 174], ['Russia', 'ru', 175], ['Rwanda', 'rw', 176], ['Saint Barthelemy', 'bl', 177], ['Saint Helena', 'sh', 178], ['Saint Kitts and Nevis', 'kn', 179], ['Saint Lucia', 'lc', 180], ['Saint Martin', 'mf', 181], ['Saint Pierre and Miquelon', 'pm', 182], ['Saint Vincent and the Grenadines', 'vc', 183], ['Samoa', 'ws', 184], ['San Marino', 'sm', 185], ['Sao Tome and Principe', 'st', 186], ['Saudi Arabia', 'sa', 187], ['Senegal', 'sn', 188], ['Serbia', 'rs', 189], ['Seychelles', 'sc', 190], ['Sierra Leone', 'sl', 191], ['Singapore', 'sg', 192], ['Sint Maarten', 'sx', 193], ['Slovakia', 'sk', 194], ['Slovenia', 'si', 195], ['Solomon Islands', 'sb', 196], ['Somalia', 'so', 197], ['South Africa', 'za', 198], ['South Korea', 'kr', 199], ['South Sudan', 'ss', 200], ['Spain', 'es', 201], ['Sri Lanka', 'lk', 202], ['Sudan', 'sd', 203], ['Suriname', 'sr', 204], ['Svalbard and Jan Mayen', 'sj', 205], ['Swaziland', 'sz', 206], ['Sweden', 'se', 207], ['Switzerland', 'ch', 208], ['Syria', 'sy', 209], ['Taiwan', 'tw', 210], ['Tajikistan', 'tj', 211], ['Tanzania', 'tz', 212], ['Thailand', 'th', 213], ['Togo', 'tg', 214], ['Tokelau', 'tk', 215], ['Tonga', 'to', 216], ['Trinidad and Tobago', 'tt', 217], ['Tunisia', 'tn', 218], ['Turkey', 'tr', 219], ['Turkmenistan', 'tm', 220], ['Turks and Caicos Islands', 'tc', 221], ['Tuvalu', 'tv', 222], ['U.S. Virgin Islands', 'vi', 223], ['Uganda', 'ug', 224], ['Ukraine', 'ua', 225], ['United Arab Emirates', 'ae', 226], ['United Kingdom', 'gb', 227], ['United States', 'us', 228], ['Uruguay', 'uy', 229], ['Uzbekistan', 'uz', 230], ['Vanuatu', 'vu', 231], ['Vatican', 'va', 232], ['Venezuela', 've', 233], ['Vietnam', 'vn', 234], ['Wallis and Futuna', 'wf', 235], ['Western Sahara', 'eh', 236], ['Yemen', 'ye', 237], ['Zambia', 'zm', 238], ['Zimbabwe', 'zw', 239]]
staff = [813441664617939004, 855793126958170122, 853997809212588073, 504029508295196683, 660353231565619200, 482612710018908190, 753869126522503310]
accepted = [813786315530305536, 813527378088951809, 813527377736761384, 813452412810690600, 813441662588157952, 836427405656326165, 853997809212588073]

usercmds = {}
saycmd = {}
lastdata = {"time":0}

error_embed = 16730441
embedcolor = 5046208
success_embed = 5963593
localembed = 16734606
economyerror = "❌"
economysuccess = "✅"
loading = "<a:loading:862916076769378304>"
color = 7929797
sampfp = "https://media.discordapp.net/attachments/854008993248051230/854708889059852288/sam_av.png"

@bot.check
async def if_allowed(ctx):
    if bot.apidown: await load_peeps()
    if bot.beta: return True
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
    if time.time() - lastdata["time"] < 5:
        return lastdata["data"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kr.vercel.app/api/clan?clan={clan}", timeout=aiohttp.ClientTimeout(total=10)) as data:
                if data.status != 200:
                    return "error"
                res = json.loads(await data.text())
                lastdata["time"] = time.time()
                lastdata["data"] = res
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

async def close_admin():
    chl = bot.get_channel(854692793276170280)
    with open("admin.json", "w") as f:
        f.write(json.dumps(bot.refr))
    await chl.send(file=discord.File("admin.json"))

async def updateuserdata():
    chl = bot.get_channel(856070919033978932)
    with open("userdata.json", "w") as f:
        f.write(json.dumps(bot.userdata, indent=2))
    await chl.send(file=discord.File("userdata.json"))

@tasks.loop(minutes=5.0)
async def auto_update():
    await update_embeds("VNTA")

@tasks.loop(minutes=1)
async def warslogs():
    exptime = bot.refr.get("cwtime_s")
    exptime2 = bot.refr.get("cwtime_e")
    if (exptime2 is None) or (exptime is None): return
    if exptime < time.time() < exptime2:
        kills, data = await end(clan="VNTA", via=True)
        if kills == 0:
            return
        today = datetime.date.today()
        d1 = today.strftime("%d-%m-%Y")
        bot.cwdata[d1] = data
        await updatecwdata()

@bot.command()
@commands.is_owner()
async def logwar(ctx):
    kills, data = await end(clan="VNTA", via=True)

    today = datetime.date.today()
    d1 = today.strftime("%d-%m-%Y")
    bot.cwdata[d1] = data
    await updatecwdata()
    await ctx.message.add_reaction(economysuccess)

async def updatecwdata():
    with open("cwdata.json", "w") as f:
        f.write(json.dumps(bot.cwdata, indent=2))
    await bot.get_channel(862972949069955083).send(file=discord.File("cwdata.json"))

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
    embed.set_author(name=user.name, icon_url=user.avatar.url)
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
            if not any(allow in [role.id for role in ctx.author.roles] for allow in staff):
                print("not qual")
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
            await ctx2.message.clear_reaction(loading)
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
            if not any(allow in [role.id for role in ctx.author.roles] for allow in staff):
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
    data = await getdata(clan)
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
            active_con = discord.Embed(description=f"```css\n{active.get_string()[count:2000]}```",
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
@commands.is_owner()
async def test(ctx):
    copy_d = copy.copy(bot.links)
    new = {}
    for i in copy_d.keys():
        new[i] = copy_d[i]["main"]
    bot.links.clear()
    bot.links = new
    await update_links()

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
    oldflag = userdata["data"]["stats"]["flg"]
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
    if ctx.author.id not in staff+devs: return

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
    if ctx.author.id not in staff+devs: return

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
    await ctx.message.add_reaction(loading)
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
    if not found:
        bgdata = bot.bgdata["vntasam123"]
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
        bgdata["file"] = bot.bgdata["vntasam123"]["file"]
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
                    embed = discord.Embed(description="Upload the `PNG/GIF` file from your PC to set as background.\n"
                                                      "**Dont send a link to the image! Upload the file**",
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
    msg = await ctx.send('Pong!')
    ping = "{:.2f}".format(bot.latency*1000)
    await msg.edit(content=f'Pong! `{ping} ms`')

@bot.command(aliases=["app"])
@commands.is_owner()
async def application(ctx):
    embed = discord.Embed(title="VNTA Applications",
                          description="Click on the button below to start the application process!",
                          color=localembed)
    await ctx.send(view=PersistentView(), embed=embed)

async def pubs(data):
    if data.user.id in bot.interlist:
        a = await data.response.send_message("You recently applied before. Please wait before re-applying", ephemeral=True)
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
        await user.send("You are not linked to VNTA bot. Please go to <#845682300967714831> and type `v.link <your ign>`.\n"
                        "After linking, you can restart this process from <#845682300570304546>")
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
        await user.send("You didnt reply in time.")

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
                scoreweek = int((score/daysplayed)/7)

                score = 0
                economysuccess = "✔️"
                embed = discord.Embed(title=f"{username}", color=localembed)
                if level >= 60:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

                if float(kdr) >= 4:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

                if float(kpg) >= 16:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

                if nukes >= 100:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)

                if scoreweek >= 100000:
                    mark = economysuccess
                    score += 1
                else: mark = economyerror
                embed.add_field(name=f"\\{mark} Score/week", value=str(scoreweek), inline=False)
                p = False
                if score == 5:
                    res = f"\\{economysuccess} QUALIFIED \\{economysuccess}"
                    p = True
                elif 3 <= score <= 4:
                    res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
                    p = True
                else:
                    res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
                embed.add_field(name="Result", value=res, inline=False)
                rescode = hex(random.randint(1000, 9999)).lower()
                allapps = bot.refr.setdefault("apps", [])
                allapps.append({rescode:{"kdr":kdr, "level":level, "kpg":kpg, "username":username, "nukes":nukes, "scoreweek":scoreweek}})
                bot.refr["apps"] = allapps
                await close_admin()
                if p:
                    embed.add_field(name="What to do now?", value=f"Head over to <#845682300967714831>, and type `v.result {rescode}`.\n"
                                                                  "A new ticket will be opened with your result posted."
                                                                  " The staff will guide you after that.", inline=False)
                embed.set_footer(text="#vantalizing")
                embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/l8ile3RBeJ7FZELTOiecL6LMUQz5qmExL8ELzQFuEag/https/media.discordapp.net/attachments/817374020810178583/838450855648690226/vnta_logo_png.png")
                await fetch.edit(embed=embed, content=None)

async def cc(data):
    if data.user.id in bot.interlist:
        a = await data.response.send_message("You recently applied before. Please wait before re-applying", ephemeral=True)
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

        embed = discord.Embed(title="Step I",
                              description="Please authorize to the bot here: [Auth URL](https://vnta.herokuapp.com/)",
                              colour=localembed)
        embed.set_footer(text="When done, react below to confirm")
        em = await user.send(embed=embed)
        await em.add_reaction(success_embed)

        def check(reaction, user_):
            return user_ == user and str(reaction.emoji) == economysuccess

        reaction, user_ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        yt, twitch = False, False
        usercons = bot.refr["con"].get(str(user.id), [])
        for cons in usercons:
            if cons["type"] == "youtube": yt = True
            if cons["type"] == "twitch": twitch = True
        if (not yt) and (not twitch):
            return await user.send("You do not have YouTube or Twitch linked. Please link them and try again")

    except:
        pass

async def comp(data):
    try:
        await data.user.send("You clicked 'Competitive'")
        await data.response.send_message("Application process started in DMs", ephemeral=True)
    except:
        return await data.response.send_message("Please open your DMs for starting the process", ephemeral=True)

async def wars(data):
    try:
        await data.user.send("You clicked 'Clan Wars'")
        await data.response.send_message("Application process started in DMs", ephemeral=True)
    except:
        return await data.response.send_message("Please open your DMs for starting the process", ephemeral=True)

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
            break
    if not found: return await ctx.reply("Invalid code or ticket already opened")
    await ctx.message.delete()
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.get_role(853997809212588073): discord.PermissionOverwrite(read_messages=True),
        bot.get_user(ctx.author.id): discord.PermissionOverwrite(read_messages=True)
    }
    num = bot.refr.setdefault("appcount", 0)
    channel = await guild.create_text_channel(f'open-appl-{num+1}', overwrites=overwrites,
                                              category=bot.get_channel(853973632153944064))
    bot.refr["appcount"] = num + 1
    score = 0
    economysuccess = "✔️"

    level = userapp["level"]
    kdr = userapp["kdr"]
    kpg = userapp["kpg"]
    nukes = userapp["nukes"]
    scoreweek = userapp["scoreweek"]

    embed = discord.Embed(title=userapp["username"], colour=localembed)
    if level >= 60:
        mark = economysuccess
        score += 1
    else:
        mark = economyerror
    embed.add_field(name=f" \\{mark} Level", value=str(level), inline=False)

    if float(kdr) >= 4:
        mark = economysuccess
        score += 1
    else:
        mark = economyerror
    embed.add_field(name=f"\\{mark} KDR", value=str(kdr), inline=False)

    if float(kpg) >= 16:
        mark = economysuccess
        score += 1
    else:
        mark = economyerror
    embed.add_field(name=f"\\{mark} KPG", value=str(kpg), inline=False)

    if nukes >= 100:
        mark = economysuccess
        score += 1
    else:
        mark = economyerror
    embed.add_field(name=f"\\{mark} Nukes", value=str(nukes), inline=False)

    if scoreweek >= 100000:
        mark = economysuccess
        score += 1
    else:
        mark = economyerror
    embed.add_field(name=f"\\{mark} Score/week", value=str(scoreweek), inline=False)
    if score == 5:
        res = f"\\{economysuccess} QUALIFIED \\{economysuccess}"
    elif 3 <= score <= 4:
        res = f"<a:Unknown:849189167522381834> TO BE TESTED <a:Unknown:849189167522381834>"
    else:
        res = f"\\{economyerror} NOT QUALIFIED \\{economyerror}"
    embed.add_field(name="Result", value=res)
    embed.add_field(name="\u200b", value="React with 🔒 to close the ticket", inline=False)
    msg = await channel.send(f"{ctx.author.mention} Please wait for a staff to respond.", embed=embed)
    opent = bot.refr.setdefault("opent", [])
    opent.append(msg.id)
    bot.refr["opent"] = opent
    await msg.add_reaction("🔒")
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/stopwatch/stopwatch_PNG140.png")

            return await ctx.send(embed=embed)
        embed = discord.Embed(title="Your Reminders",
                              color=localembed)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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
            autrems.append({"tadd":time.time(), "desc":desc, "time":secs, "id":remid+1, "chl":ctx.channel})
            allrems[str(ctx.author.id)] = autrems
            bot.refr["rems"] = allrems
            await msg_.delete()
            embed = discord.Embed(title="Add a reminder",
                                  description=f"Done! I will remind you at <t:{int(time.time() + secs)}:F> ;)",
                                  colour=localembed)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
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

@bot.command()
@commands.is_owner()
async def load_peeps(ctx=None):
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
                if ctx is not None:
                    await ctx.message.add_reaction(economysuccess)
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
@commands.is_owner()
async def apidata(ctx):
    await ctx.send(f"```json\n{bot.refr['con']}```")

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
async def suggest(ctx, *, sug):
    stfchl = bot.get_channel(813447381752348723)
    embed = discord.Embed(title="Suggestion Approval",
                          description=sug,
                          color=localembed)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    em = await stfchl.send(embed=embed)
    bot.suggestions[em.id] = (ctx.author.id, sug)
    await em.add_reaction(economysuccess)
    await em.add_reaction(economyerror)
    await ctx.message.add_reaction(economysuccess)

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
async def cw(ctx, *, ign):
    pass

@bot.command()
@commands.is_owner()
async def enable(ctx, cmd):
    bot.refr["dcmds"].pop(cmd)
    await ctx.message.add_reaction(economysuccess)
    await close_admin()

@bot.command(aliases=["ref"])
async def load_data(ctx=None):
    chl = bot.get_channel(854692793276170280)
    msgs = await chl.history(limit=1).flatten()
    bot.refr = json.loads(requests.get(msgs[0].attachments[0]).text)
    bot.cwpause = bot.refr["cwpause"]
    bot.pause = bot.refr["pause"]

    chl = bot.get_channel(854721559359913994)
    msgs = await chl.history(limit=1).flatten()
    bot.links.update(json.loads(requests.get(msgs[0].attachments[0]).text))

    chl = bot.get_channel(856070919033978932)
    msgs = await chl.history(limit=1).flatten()
    bot.userdata = json.loads(requests.get(msgs[0].attachments[0]).text)

    chl = bot.get_channel(854698116255318057)
    msgs = await chl.history(limit=1).flatten()
    bot.bgdata = json.loads(requests.get(msgs[0].attachments[0]).text)

    chl = bot.get_channel(862972949069955083)
    msgs = await chl.history(limit=1).flatten()
    bot.cwdata = json.loads(requests.get(msgs[0].attachments[0]).text)

    if ctx is not None:
        await ctx.message.add_reaction(economysuccess)

async def one_ready():
    print("Connected")
    await bot.wait_until_ready()
    await load_data()
    await load_peeps()
    print("Ready")
    bot.dev = bot.get_user(771601176155783198)
    bot.linkinglogs = bot.get_channel(861463678179999784)
    if not bot.pause or not bot.beta:
        if not bot.cwpause: auto_update.start()
    if not bot.beta:
        handle_rems.start()
        warslogs.start()

@bot.event
async def on_message(message):
    if bot.beta:
        if message.channel.id not in [854008993248051230, 853973674309582868, 862265264838410241, 839080243485736970]: return
    else:
        if message.channel.id == 864755738609057822:
            data = "{" + message.content + "}"
            data = dict(eval(data))
            old = bot.refr.setdefault("con", {})
            for k, v in data.items():
                old[k] = v
            bot.refr["con"] = old
            await close_admin()
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == 853971223682482226: return

    if str(payload.emoji) == "🗑️" and payload.user_id == 771601176155783198:
        chl = await bot.fetch_channel(payload.channel_id)
        msg = await chl.fetch_message(payload.message_id)
        await msg.delete()
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
            oldflag = userdata["data"]["stats"]["flg"]
            if oldflag != userd[2]:
                return await chan.send(f"{user.mention} The flag change wasn't detected. Make sure to stick to the end of the match\n"
                                       f"Retry using `v.link {userdata['data']['username']}`")
            t = bot.links.get(str(user.id), {"main":userdata['data']['username'], "all":[]})
            t["all"] = list(set(t["all"]))
            t["all"].append(userdata['data']['username'])
            bot.links[str(user.id)] = t
            await update_links()
            await chan.send(f"{user.mention} {economysuccess} You are successfully linked with `{userdata['data']['username']}`!")
            await linklog(ign=userdata['data']['username'], user=user, t="l")
        bot.pendings.pop(payload.message_id)
    if payload.channel_id == 813447381752348723 and str(payload.emoji) in [economyerror, economysuccess]:
        chan = bot.get_channel(payload.channel_id)
        userd = bot.suggestions.get(payload.message_id)
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
            embed.set_author(name=f"By: {user}", icon_url=user.avatar.url)
            em = await sugchl.send(embed=embed)
            await em.add_reaction("👍")
            await em.add_reaction("👎")
        bot.suggestions.pop(payload.message_id)
    if str(payload.emoji) == "🔒":
        if payload.message_id in bot.refr.get("opent", []):
            tchl = bot.get_channel(payload.channel_id)
            guild = bot.get_guild(payload.guild_id)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.get_role(853997809212588073): discord.PermissionOverwrite(read_messages=True)
            }
            await tchl.edit(name=f"{tchl.name.replace('open', 'closed')}", overwrites=overwrites)
            embed = discord.Embed(title="Ticket Closed",
                                  description="React with ⛔ to delete the channel",
                                  colour=localembed)
            clsd = await tchl.send(embed=embed)
            await clsd.add_reaction("⛔")
            oldclsd = bot.refr.setdefault("closet", [])
            oldclsd.append(clsd.id)
            bot.refr["closet"] = oldclsd
            new = bot.refr["opent"]
            new.remove(payload.message_id)
            bot.refr["opent"] = new
            await close_admin()
    if str(payload.emoji) == "⛔":
        if payload.message_id in bot.refr.get("closet", []):
            tchl = bot.get_channel(payload.channel_id)
            await tchl.send("Deleting in 5 secs...")
            await asyncio.sleep(5)
            await tchl.delete()

bot.loop.create_task(one_ready())
bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")


