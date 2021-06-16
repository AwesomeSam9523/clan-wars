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
bot = commands.Bot(command_prefix="cw"+" ")
color = 7929797
chls = {853973674309582868: "VNTA",
        854244917877538846: "TFFS",
        854005851717894166: "TFFS",
        854395888540450827: "VNTA",
        854008993248051230: "VNTA"}

with open("refr.json", "r") as r:
    refr = json.load(r)
#"VNTA": {"chl":854395888540450827, "act":[854418930080546856], "exp":[854418928255500308]},

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
    return json.loads(data.text)

async def embed_view(clan):
    data = await getdata(clan)
    data = data["data"]["members"]
    active = PrettyTable()
    active.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    expired = PrettyTable()
    expired.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    yet = PrettyTable()
    yet.field_names = ["S.No.", "Player Name"]
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
            actlist.append(active_con)
            break
        else:
            if count > len(active.get_string()): break
            active_con = discord.Embed(title=f'{clan}- Active Contracts',
                                   description=f"```css\n{active.get_string()[count:2000]}```",
                                   color=color)
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
            explist.append(active_con)
            break
        else:
            if count > len(expired.get_string()): break
            active_con = discord.Embed(title=f'{clan}- Expired Contracts',
                                   description=f"```css\n{expired.get_string()[count:2000]}```",
                                   color=color)
            count += 2000
            explist.append(active_con)

    return {"active":actlist, "expired":explist}

async def auto_update():
    while True:
        for i in refr.keys():
            await update_embeds(i)
        await asyncio.sleep(300)

async def update_embeds(clan):
    await bot.wait_until_ready()
    all_data = refr[clan]
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
            i.set_footer(text="Last Refreshed")
            i.timestamp = datetime.datetime.utcnow()
            await actlist[count].edit(embed=i)
    else:
        return await view(channel, "sam123", clan)

    if len(data["expired"]) == len(actlist):
        for i in data["expired"]:
            count = 0
            i.set_footer(text="Last Refreshed")
            i.timestamp = datetime.datetime.utcnow()
            await explist[count].edit(embed=i)
    else:
        return await view(channel, "sam123", clan)

@bot.command()
async def view(channel, via=None, clan=None):
    if via == "sam123" and clan is not None:
        pass
    else:
        channel = channel.channel
    data = await embed_view(chls[channel.id])
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
        refr[clan] = maybeupdate
        with open("refr.json", "r") as r:
            refrold = json.load(r)
        with open("refr.json", "w") as r:
            r.write(json.dumps(refr, indent=2))
        await update_embeds(clan)

@bot.command()
async def refresh(ctx, what:str=None):
    clan = chls[ctx.channel.id]
    if what is None:
        await update_embeds(clan)
        await ctx.message.add_reaction("✅")
    elif what == "setup":
        await view(ctx.channel, "sam123", clan)

@bot.command()
async def end(ctx):
    return
    chls = {853973674309582868: "VNTA",
            854005851717894166: "TFFS",
            854008993248051230: "VNTA"}
    data = await getdata()
    data = data[3]["p"]
    x = PrettyTable()
    x.field_names = ["S.No.", "Player Name", "Kills", "Estd. Kills", "Time Played"]
    sno = 1
    finalkills = 0
    for i in data:
        if i["c"] == chls[ctx.channel.id]:
            timeplayed = int(i["tp"] / 1000)
            finalkills += i["k"]
            if timeplayed > 10800:
                continue
            left = datetime.timedelta(seconds=timeplayed)
            final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
            colon_format = str(final).split(" ")[1].split(':')
            est = int(i["k"]/timeplayed)*10800
            x.add_row([str(sno) + ".", i["p"], i["k"], est, f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
            sno += 1
    x.sortby = "Kills"
    x.reversesort = True
    embed = discord.Embed(title=f'{chls[ctx.channel.id]}- Estimated Kills',
                          description=f"```css\n{x}```",
                          color=color)
    embed.set_footer(text=f"Estimated Ending: {finalkills}")
    await ctx.send(embed=embed)

@bot.event
async def on_connect():
    print("Connected")
    asyncio.create_task(auto_update())

bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")
