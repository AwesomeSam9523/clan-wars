from quart import Quart
from discord.ext import ipc


app = Quart(__name__)
ipc_client = ipc.Client(secret_key="NUJl5Q5K2_db7DTS9BX8oa8c7Fc4K6te")  # secret_key must be the same as your server


@app.route("/")
async def index():
    member_count = await ipc_client.request(
        "get_member_count", guild_id=719946380285837322
    )  # get the member count of server with ID 12345678

    print(member_count)  # display member count


if __name__ == "__main__":
    app.run()