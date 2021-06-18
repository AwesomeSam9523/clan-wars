import ssl, msgpack, asyncio, discord, json
import time, datetime, os, threading, requests
from prettytable import PrettyTable
from discord.ext import commands

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
bot = commands.Bot(command_prefix=["cw"+" ", "Cw"+" ", "cW"+" ","CW"+" "], case_insensitive=True)
bot.remove_command("help")
color = 7929797
sampfp = "https://media.discordapp.net/attachments/854008993248051230/854708889059852288/sam_av.png"
bot.refr = {}
bot.links = {}
bot.data = {}
bot.dev = ""

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
    active.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    expired = PrettyTable()
    expired.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    act = 1
    exp = 1
    yets = 1
    for i in data:
        j = i
        i = i["contract"]
        timeplayed = int(i["timeplayed"] / 1000)
        left = datetime.timedelta(seconds=timeplayed)
        final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
        colon_format = str(final).split(" ")[1].split(':')

        if timeplayed < 10800 and timeplayed != 0:
            active.add_row([str(act) + ".", j["username"], i["kills"], i["deaths"],
                            f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            act += 1

        elif timeplayed >= 10800:
            expired.add_row([str(exp) + ".", j["username"], i["kills"], i["deaths"],
                             f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            exp += 1
    active.sortby = "Kills"
    active.reversesort = True
    actlist = []
    explist = []

    count = 0
    while True:
        if len(active.get_string()) <= 2000:
            active_con = discord.Embed(title=f'{clan}- Active Contracts',
                                   description=f"```css\n{active}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            actlist.append(active_con)
            break
        else:
            if count > len(active.get_string()): break
            active_con = discord.Embed(title=f'{clan}- Active Contracts',
                                   description=f"```css\n{active.get_string()[count:2000]}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            count += 2000
            actlist.append(active_con)

    expired.sortby = "Kills"
    expired.reversesort = True
    count = 0
    while True:
        if len(expired.get_string()) <= 2000:
            active_con = discord.Embed(title=f'{clan}- Expired Contracts',
                                   description=f"```css\n{expired}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            explist.append(active_con)
            break
        else:
            if count > len(expired.get_string()): break
            active_con = discord.Embed(title=f'{clan}- Expired Contracts',
                                   description=f"```css\n{expired.get_string()[count:2000]}```",
                                   color=color)
            active_con.set_footer(text=f"Bot by {bot.dev}", icon_url=sampfp)
            count += 2000
            explist.append(active_con)

    return {"active":actlist, "expired":explist}

async def auto_update():
    while True:
        for i in bot.refr.keys():
            await update_embeds(i)
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
        return await view(channel, "sam123", clan)

    if len(data["expired"]) == len(actlist):
        for i in data["expired"]:
            count = 0
            i.set_footer(text=f"Bot by {bot.dev} | Last Refreshed", icon_url=sampfp)
            i.timestamp = datetime.datetime.utcnow()
            await explist[count].edit(embed=i)
    else:
        return await view(channel, "sam123", clan)

async def update_links():
    with open("links.json", "w") as f:
        f.write(str(json.dumps(bot.links, indent=2)))
    await bot.get_channel(854721559359913994).send(file=discord.File("links.json"))

@bot.command()
async def view(channel, via=None, clan=None):
    if via == "sam123" and clan is not None:
        pass
    else:
        if not any(allow in [role.id for role in channel.author.roles] for allow in accepted):
            return await channel.reply("Only VNTA members are given the exclusive rights to use the bot.")
        channel = channel.channel
    data = await embed_view("VNTA")
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
@commands.has_permissions(manage_channels=True)
async def refresh(ctx, what:str=None):
    clan = "VNTA"
    if what is None:
        await update_embeds(clan)
        await ctx.message.add_reaction("✅")
    elif what == "setup":
        await view(ctx.channel, "sam123", clan)
        chl = bot.get_channel(854692793276170280)
        await chl.send(str(json.dumps(bot.refr)))

@bot.command()
async def end(ctx):
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    clan = "VNTA"
    data = await getdata("VNTA")
    data = data["data"]["members"]
    active = PrettyTable()
    active.field_names = ["S.No.", "Player Name", "Kills", "Estd. Kills", "Time Played"]
    sno = 1
    finalkills = 0
    act = 1
    exp = 1
    fianlkills = 0
    for i in data:
        j = i
        i = i["contract"]
        timeplayed = int(i["timeplayed"] / 1000)
        left = datetime.timedelta(seconds=timeplayed)
        final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
        colon_format = str(final).split(" ")[1].split(':')
        finalkills += i["kills"]
        if timeplayed == 0:
            est = 0
        else:
            est = int((i["kills"]/timeplayed)*10800)
        if timeplayed < 10800 and timeplayed != 0:
            active.add_row([str(act) + ".", j["username"], i["kills"], est,
                            f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            act += 1

    active.sortby = "Kills"
    active.reversesort = True
    actlist = []
    explist = []

    count = 0
    while True:
        if len(active.get_string()) <= 2000:
            active_con = discord.Embed(title=f'{clan}- Active Contracts',
                                       description=f"```css\n{active}```",
                                       color=color)
            actlist.append(active_con)
            break
        else:
            if count > len(active.get_string()): break
            active_con = discord.Embed(title=f'{clan}- Active Contracts',
                                       description=f"```css\n{active.get_string()[count:2000]}```",
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
    except Exception as e:
        await ctx.reply(f'```\n{e}```')

@bot.command(aliases=['exec'],hidden=True)
@commands.is_owner()
async def execute(ctx, *, expression):
    try:
        exec(expression.replace('```', ''))
    except Exception as e:
        await ctx.reply(f'Command:```py\n{expression}```\nOutput:```\n{e}```')

accepted = [813786315530305536, 813527378088951809, 813527377736761384, 813452412810690600, 813441662588157952, 836427405656326165, 853997809212588073]
@bot.command()
@commands.is_owner()
async def test(ctx):
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    guild = await bot.fetch_guild(719946380285837322)
    print(guild.roles)
    for role in guild.roles:
        if "VNTA" in role.name:
            print(role.id, role.name)

@bot.command()
async def link(ctx, *, ign):
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    bot.links[str(ctx.author.id)] = str(ign)
    embed = discord.Embed(description=f"✅ Linked successfully!", color=5963593)
    await ctx.reply(embed=embed)
    await update_links()

@bot.command(aliases=["con"])
async def contract(ctx, *, ign=None):
    if not any(allow in [role.id for role in ctx.author.roles] for allow in accepted):
        return await ctx.reply("Only VNTA members are given the exclusive rights to use the bot.")
    if ign is None:
        ign = bot.links.get(str(ctx.author.id))
        if ign is None:
            embed = discord.Embed(description="You aren't linked yet. Use `cw link <ign>` to get linked.\n"
                                              "Or use `cw contract <ign> to view",
                                  color=16730441)
            embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing")
            return await ctx.reply(embed=embed)
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
    final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
    colon_format = str(final).split(" ")[1].split(':')
    games = timeplayed / 240
    if timeplayed == 0:
        est = 0
        kpg = 0
    else:
        est = int(con["kills"] / timeplayed) * 10800
        kpg = con["kills"]/games
    x = PrettyTable()
    x.field_names = ["Kills", "Deaths", "KPG", "Est Kills", "Play Time"]
    x.add_row([con["kills"], con["deaths"], "{:.2f}".format(kpg), est, f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
    embed = discord.Embed(title=f"CW Contract- {userdata['username']}",
                          description=f"```css\n{x}```",
                          color=4521960)
    embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing", icon_url=sampfp)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="VNTA Clan Wars Bot",
                        description="View below the commands available for use:",
                        color=4849598)
    embed.add_field(name="`link`", value="Syntax: `cw link <ign>`\nLink account to bot", inline=False)
    embed.add_field(name="`contract`", value="Syntax: `cw contract [ign]`\nShows clan war contract", inline=False)
    embed.set_footer(text=f"Bot by {bot.dev} | #vantalizing", icon_url=sampfp)
    await ctx.send(embed=embed)

@bot.event
async def on_connect():
    print("Connected")
    await bot.wait_until_ready()
    chl = bot.get_channel(854692793276170280)
    msgs = await chl.history(limit=1).flatten()
    bot.refr = json.loads(msgs[0].content)

    chl = bot.get_channel(854721559359913994)
    msgs = await chl.history(limit=1).flatten()
    bot.links.update(json.loads(requests.get(msgs[0].attachments[0]).text))
    bot.dev = await bot.fetch_user(771601176155783198)
    print("Ready")
    asyncio.create_task(auto_update())

bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")
