import ssl, msgpack, asyncio, websockets, discord, json
import time, datetime, os
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
async def getdata():
    ssl_context = ssl._create_unverified_context()
    async with websockets.connect(uri=uri, extra_headers=a_headers, ssl=ssl_context) as websocket:
        data = msgpack.packb(["r", "clanwars", "Q", None, None, None, "0", None], use_bin_type=True) + b"\x00\x00"
        await websocket.send(data)
        while True:
            response_data = msgpack.unpackb((await websocket.recv())[0:-2], raw=False)
            if response_data[0] == "news": continue
            elif response_data[0] == "cpt":
                os.system("node cpt/index.js")
            elif response_data != ["pi"]: break
        return response_data

@bot.command()
async def view(ctx):
    chls = {853973674309582868: "VNTA",
            854005851717894166: "TFFS",
            854008993248051230: "VNTA"}
    data = await getdata()
    print(data)
    data = data[3]["p"]
    active = PrettyTable()
    active.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]

    expired = PrettyTable()
    expired.field_names = ["S.No.", "Player Name", "Kills", "Deaths", "Time Played"]
    act = 1
    exp = 1
    for i in data:
        if i["c"] == chls[ctx.channel.id]:
            timeplayed = int(i["tp"]/1000)
            left = datetime.timedelta(seconds=timeplayed)
            final = datetime.datetime.strptime(str(left), '%H:%M:%S').replace(microsecond=0)
            colon_format = str(final).split(" ")[1].split(':')
            if timeplayed < 10800:
                active.add_row([str(act) + ".", i["p"], i["k"], i["d"], f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
                act += 1
            else:
                expired.add_row([str(exp) + ".", i["p"], i["k"], i["d"],
                                f"{colon_format[0]}h {colon_format[1]}m {colon_format[2]}s"])
                exp += 1
    active.sortby = "Kills"
    active.reversesort = True
    embed1 = discord.Embed(title=f'{chls[ctx.channel.id]}- Active Contracts',
                          description=f"```css\n{active}```",
                          color=color)

    expired.sortby = "Kills"
    expired.reversesort = True
    embed2 = discord.Embed(title=f'{chls[ctx.channel.id]}- Finished Contracts',
                          description=f"```css\n{expired}```",
                          color=color)
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

@bot.command()
async def end(ctx):
    chls = {853973674309582868: "VNTA",
            854005851717894166: "TFFS",
            854008993248051230: "VNTA"}
    data = await getdata()
    data = data[3]["p"]
    x = PrettyTable()
    x.field_names = ["S.No.", "Player Name", "Kills", "Estd. Kills", "Time Played"]
    sno = 1
    for i in data:
        if i["c"] == chls[ctx.channel.id]:
            timeplayed = int(i["tp"] / 1000)
            if timeplayed > 10800: continue
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
    await ctx.send(embed=embed)

print("Running...")
bot.run("ODUzOTcxMjIzNjgyNDgyMjI2.YMdIrQ.N-06PP7nmUz-E-3bQvWqCtArhP0")
