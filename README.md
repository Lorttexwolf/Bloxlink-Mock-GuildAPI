# Bloxlink Mock GuildAPI
The GuildAPI is a concept that has been under consideration. So, I've created a limited but simple example of its usage, and possible implementation.

> **Note**:
> This project is not intended to be utilized, it is simply an example.

## Limited Scope of the GuildAPI 🔒
Currently, there are several downsides to the current iteration of the API: harsh base global rate limits and lack of reverse-lookup due to the current global scope.
The GuildAPI aims to address and solve some of these issues by requiring your `api-key` to be limited to certain applications/bots, ensuring that a users privacy wouldn't be a worry (like an integration with your server).
Because of this limited scope of data the end-developer/bot can access, this should reduce rate limits to guilds, not globally. In addition, it may be acceptable to publicly offer the reverse-search API.
  
## Installation ⚙️
Firstly, you'll need to install the dependencies: `pip install sanic requests`

### Environment 
Before you start, you'll need to configure some environment variables.
* Copy the `.env.example` file and rename it to `.env`. 
* `BLOXLINK_BOT_TOKEN` Intended for the Bloxlink bot.
* `BLOXLINK_API_TOKEN` Bloxlink API token.

These keys are intended to be stored in MongoDB.
* `USER_API_TOKEN` The `api-key` header value used to simulate authentication.
* `USER_BOT_ID` The end-developers application/bot, the core of the guild scope.

You're all set, run `python3 ./src/main.py`

## Endpoint Usage
Compared to the current API, these endpoints require a guild to be provided.

`http://127.0.0.1:8001/guild/{guildId}/member/{userId}`
> Retrieves the linked Roblox account of the member in a guild.
> * If the associated application/bot of the key is not in the guild, `403 (Forbidden)` will be returned.
> * If this user isn't in the guild, `204 (No Content)` will be returned. 
