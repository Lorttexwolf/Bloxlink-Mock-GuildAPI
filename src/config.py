import os
from dotenv import load_dotenv
from pathlib import Path

# Escaping into the parent dir will be the working directory at runtime. 
load_dotenv(Path('.env'))

# Sanic has its own config manager, but lets keep it simple.
DISCORD_BOT_TOKEN = os.getenv("BLOXLINK_BOT_TOKEN")
USER_BOT_ID = os.getenv("USER_BOT_ID")
USER_API_TOKEN = os.getenv("USER_API_TOKEN")
BLOXLINK_API_TOKEN = os.getenv("BLOXLINK_API_TOKEN")

# Ensure all required environment variables exist.
for eVariable in [DISCORD_BOT_TOKEN, USER_BOT_ID, USER_API_TOKEN, BLOXLINK_API_TOKEN]:
    if eVariable == None:
        raise EnvironmentError(f"Missing required environment variable!")