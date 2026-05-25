# Insectobot

A Discord bot to simulate "beetle draw" for Insectopia Table-Top RPG.

## Installation

You must add to the cloned repository a file named 'env.py', containing :
```py
BOT_TOKEN = {BOT_TOKEN}
GUILD_ID = {GUILD_ID}
```
Replacing `{BOT_TOKEN}` by the bot token and `{GUILD_ID}` by the ID of the server hosting your bot.

## Running

Start the but by running in the repository :
```
python3 -u main.py
```

Then, in your server, the bot should answer the following commands :
* `/language {LANGUAGE}` to set the bot language. `{LANGUAGE}` must be either French or English (expressed in either French or English).
* `/draw {COUNT} {BONUS}` to draw beetles. `{COUNT}` must be between 1 and 42. `{BONUS}` is optional, and can be positive or negative.
* `/born` simulate a complete draw for a new character, drawing a beetle for each characteristic.
