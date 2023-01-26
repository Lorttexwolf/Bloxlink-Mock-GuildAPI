from config import DISCORD_BOT_TOKEN
import requests 

requestHeaders = {
    "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
}

# def get_guild(guildId: str):
#     res = requests.get(f"https://discord.com/api/v9/guilds/{guildId}", headers=requestHeaders)
#     return res.json() if res.status_code == 200 else None

def get_guild_member(guildId: str, userId: str):
    res = requests.get(f"https://discord.com/api/v9/guilds/{guildId}/members/{userId}", headers=requestHeaders)
    
    return res.json() if res.status_code == 200 else None