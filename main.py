import discord
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def print_usage(channel, message):
    usage = "Usage: `!draw [count]`"
    if message:
        usage = f"{message}\n{usage}"
    await channel.send(usage)

async def read_count(message, channel):
    message_args = message.split(' ')[1:]
    if len(message_args) != 1:
        await print_usage(channel, "Invalid args count.")
        return None

    if not message_args[0].isnumeric():
        await print_usage(channel, "Invalid argument: not a number.")
        return None

    return int(message_args[0])

def draw_numbers(count):
    numbers = []
    for i in range(count):
        number = random.randrange(0, 42)
        while number in numbers:
            number = random.randrange(0, 42)
        numbers.append(number)
    return numbers

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!draw"):
        count = await read_count(message.content, message.channel)
        if count is None:
            return

        if count < 1 or count > 42:
            await print_usage(message.channel, "Invalid argument: count must be between 1 and 42.")
            return

        numbers = draw_numbers(count)
        answer = "You have drawn:\n"
        for number in numbers:
            if number < 3:
                answer += " • a :black_circle: (critical failure)\n"
            elif number >= 3 and number < 21:
                answer += " • a :white_circle: (failure)\n"
            elif number >= 21 and number < 33:
                answer += " • a :blue_circle: (success)\n"
            elif number >= 33 and number < 39:
                answer += " • a :green_circle: (improved success)\n"
            elif number >= 39:
                answer += " • a :red_circle: (critical success)\n"
        await message.channel.send(answer)

client.run("MTAzMDU4MDg4OTA5NDIxMzY4Mg.GAo39R.axAkfXOfv5WZTq7xdShGqjA7nbQKUPjy8VImi0")
