from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, jsonify, make_response
import os, random

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

base_discord_api_url = 'https://discordapp.com/api'
client_id = r'853971223682482226' # Get from https://discordapp.com/developers/applications
client_secret = 'NUJl5Q5K2_db7DTS9BX8oa8c7Fc4K6te'
redirect_uri='https://vnta.herokuapp.com/oauth_callback'
scope = ['identify', 'connections']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.route("/")
def home():
    """
    Presents the 'Login with Discord' link
    """
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session["state"] = state
    return redirect(redirect_uri)

@app.route("/oauth_callback")
def oauth_callback():
    """
    The callback we specified in our app.
    Processes the code given to us by Discord and sends it back
    to Discord requesting a temporary access token so we can 
    make requests on behalf (as if we were) the user.
    e.g. https://discordapp.com/api/users/@me
    The token is stored in a session variable, so it can
    be reused across separate web requests.
    """
    try:
        state = session["state"]
        print('Got state', state)
    except KeyError:
        print('KeyError Detected, Redirecting...')
        return redirect('https://vnta.herokuapp.com/')

    discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=state, scope=scope)

    token = discord.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['discord_token'] = token
    discord2 = OAuth2Session(client_id, token=token)
    userinfo = discord2.get(base_discord_api_url + '/users/@me')
    connections = discord2.get(base_discord_api_url + '/users/@me/connections')
    print(userinfo.json())
    print(connections.json())
    return f'Done!'

if __name__ == '__main__':
    print('Running')
    app.run(port=8000)

