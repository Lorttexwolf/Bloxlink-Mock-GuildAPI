
from config import USER_API_TOKEN, USER_BOT_ID, BLOXLINK_API_TOKEN
from sanic import Sanic, HTTPResponse
from sanic.response import text, json
import discord
import requests


app = Sanic("BloxlinkMockGuildAPI")

@app.route("/guild/<guildId:int>/member/<userId:int>", methods=["GET"])
async def get_guild_roblox_member(req, guildId, userId):
    # Ensure the associated user and bot of the api-key are in the requested guild.
    if discord.get_guild_member(guildId, USER_BOT_ID) == None:
        return HTTPResponse(status=403)
    if discord.get_guild_member(guildId, userId) == None:
        return HTTPResponse(status=204)

    # Could be separated into a module but we need the response headers. 
    userReq = requests.get(f"https://v3.blox.link/developer/discord/{userId}?guildId={guildId}", headers={"api-key": BLOXLINK_API_TOKEN})
    if userReq.status_code == 200:
        # Sorta acting like a reverse proxy, but instead we are just returning the quota. (not optimal)
        # Additionally, this is where scoped rate-limits would be implemented. 
        return json(userReq.json(), headers={
            "quota-remaining": userReq.headers.get("quota-remaining")
        })
    else:
        return text(status=204)

@app.middleware("request")
async def request_middleware(req):
    # Middleware ensures that appropriate authorization of the api-token is met.
    apiKey = req.headers.get('api-key')
    if apiKey != USER_API_TOKEN:
        return text("You are not authorized.", status=401)
    
if __name__ == '__main__':
    app.register_middleware(lambda req: req.headers.get("api-token") == USER_API_TOKEN)
    app.run('127.0.0.1', 8001, debug=True)