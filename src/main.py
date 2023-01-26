from config import USER_API_TOKEN, USER_BOT_ID, BLOXLINK_API_TOKEN
from sanic import Sanic, HTTPResponse
from sanic.response import text, json
import discord
import requests


app = Sanic("BloxlinkMockGuildAPI")

def member_accessibility_code(guildId: str, discordUserId: str) -> int:
    '''Determines if the requested guild member can be accessed.'''
    if not discord.get_guild_member(guildId, USER_BOT_ID):
        return 403 # Forbidden
    elif not discord.get_guild_member(guildId, discordUserId):
        return 204 # No Content
    else:
        return 200

@app.route("/guild/<guildId:int>/member/<discordUserId:int>", methods=["GET"])
async def get_guild_roblox_member(req, guildId, discordUserId):
    # Ensure the associated user and bot of the api-key are in the requested guild. Maintain the guild scope!
    accessibilityCode = member_accessibility_code(guildId, discordUserId) 
    if accessibilityCode != 200:
        return HTTPResponse(status=accessibilityCode)

    # Could be separated into a module but we need the response headers. 
    userReq = requests.get(f"https://v3.blox.link/developer/discord/{discordUserId}?guildId={guildId}", headers={"api-key": BLOXLINK_API_TOKEN})
    if userReq.status_code == 200:
        # Sorta acting like a reverse proxy, but instead only the quota header is included. (not optimal)
        # Additionally, this is where scoped rate-limits would be implemented. 
        return json(userReq.json(), headers={
            "quota-remaining": userReq.headers.get("quota-remaining")
        })
    else:
        return text(status=204)
    
# Reverse search endpoint.
@app.route("/guild/<guildId:int>/reversemember/<robloxUserId:int>", methods=["GET"])
async def get_roblox_guild_member(req, guildId, robloxUserId):
    # Perform a reverse search.
    discordUserId = None
    if not discordUserId:
         return HTTPResponse(status=204)
    
    # Once the discordUserId is found, the same accessibility check would be ran.
    accessibilityCode = member_accessibility_code(guildId, discordUserId) 
    if accessibilityCode != 200:
        return HTTPResponse(status=accessibilityCode)
    
    raise NotImplementedError()

@app.middleware("request")
async def request_middleware(req):
    # Middleware ensures that appropriate authorization of the api-token is met.
    apiKey = req.headers.get('api-key')
    if apiKey != USER_API_TOKEN:
        return text("You are not authorized.", status=401)
    
if __name__ == '__main__':
    app.register_middleware(lambda req: req.headers.get("api-token") == USER_API_TOKEN)
    app.run('0.0.0.0', 8001, debug=True)