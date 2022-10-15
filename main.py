import discord
import random

from enum import Enum, auto

class Color(Enum):
    Black = auto()
    White = auto()
    Blue = auto()
    Green = auto()
    Red = auto()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def print_usage(channel, message):
    usage = "Usage: `!draw [count]` or `!draw born`"
    if message:
        usage = f"{message}\n{usage}"
    await channel.send(usage)

def read_arg(message, channel):
    message_args = message.split(' ')[1:]
    if len(message_args) != 1:
        return None

    return message_args[0]

def draw_colors(count):
    numbers = []
    for i in range(count):
        number = random.randrange(0, 42)
        while number in numbers:
            number = random.randrange(0, 42)
        numbers.append(number)
    colors = []
    for number in numbers:
        if number < 3:
            colors.append(Color.Black)
        elif number >= 3 and number < 21:
            colors.append(Color.White)
        elif number >= 21 and number < 33:
            colors.append(Color.Blue)
        elif number >= 33 and number < 39:
            colors.append(Color.Green)
        elif number >= 39:
            colors.append(Color.Red)
    return colors

def color_to_emoji(color):
    return str({
        Color.Black: ":black_circle:",
        Color.White: ":white_circle:",
        Color.Blue:  ":blue_circle:",
        Color.Green: ":green_circle:",
        Color.Red:   ":red_circle:",
    }.get(color))

def color_to_success_rate(color):
    return str({
        Color.Black: "critical failure",
        Color.White: "failure",
        Color.Blue:  "success",
        Color.Green: "improved success",
        Color.Red:   "critical success",
    }.get(color))

def color_to_characteristic_change(color):
    return str({
        Color.Black: "capacity",
        Color.White: "+1 skill point",
        Color.Blue:  "+2 skill point",
        Color.Green: "+1 skill point and +1 free skill point (for any skill)",
        Color.Red:   "characteristic improved by 1",
    }.get(color))


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!draw"):
        arg = read_arg(message.content, message.channel)
        if arg is None:
            await print_usage(message.channel, "Invalid args count.")
            return

        if arg == "-h" or arg == "--help":
            await print_usage(message.channel, None)
            return

        elif arg == "born":
            answer = "You have drawn:\n"
            colors = draw_colors(7)
            characteristics = [
                "Wing",
                "Antenna",
                "Caste",
                "Chitin",
                "Spirit",
                "Mandible",
                "Temperature",
            ]
            for i in range(0, 7):
                answer += " • {0} : {1} ({2})\n".format(characteristics[i], color_to_emoji(colors[i]), color_to_characteristic_change(colors[i]))
            await message.channel.send(answer)

        elif arg.isnumeric():
            count = int(arg)
            if count < 1 or count > 42:
                await print_usage(message.channel, "Invalid argument: count must be between 1 and 42.")
                return

            colors = draw_colors(count)
            answer = "You have drawn:\n"
            for color in colors:
                answer += " • a {0} ({1})\n".format(color_to_emoji(color), color_to_success_rate(color))
            await message.channel.send(answer)

        else:
            await print_usage(channel, "Invalid argument.")
            return

client.run("MTAzMDU4MDg4OTA5NDIxMzY4Mg.GAo39R.axAkfXOfv5WZTq7xdShGqjA7nbQKUPjy8VImi0")
