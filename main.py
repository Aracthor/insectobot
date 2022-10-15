import discord
import random

from enum import Enum, auto

from localization import localization_dictionnary, Language

localization = localization_dictionnary()

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
    usage = localization.get("usage")
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
        Color.Black: localization.get("critical_failure"),
        Color.White: localization.get("failure"),
        Color.Blue:  localization.get("success"),
        Color.Green: localization.get("improved_success"),
        Color.Red:   localization.get("critical_success"),
    }.get(color))

def color_to_characteristic_change(color):
    return str({
        Color.Black: localization.get("capacity"),
        Color.White: localization.get("1_more_skill_point"),
        Color.Blue:  localization.get("2_more_skill_point"),
        Color.Green: localization.get("1_more_skill_point_and_1_more_free_skill_point"),
        Color.Red:   localization.get("characteristic_improved"),
    }.get(color))


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!language"):
        arg = read_arg(message.content, message.channel)
        if not arg:
            return

        language = arg.lower()
        languages = {
            "french": Language.French,
            "français": Language.French,
            "english": Language.English,
            "anglais": Language.English,
        }
        if not language in languages:
            await message.channel.send(localization.get("invalid_language"))
            return
        localization.set_language(languages.get(language))
        await message.channel.send(localization.get("language_set"))

    if message.content.startswith("!draw"):
        arg = read_arg(message.content, message.channel)
        if arg is None:
            await print_usage(message.channel, localization.get("invalid_arg_count"))
            return

        if arg == "-h" or arg == "--help":
            await print_usage(message.channel, None)
            return

        elif arg == "born":
            answer = localization.get("you_have_drawn")
            colors = draw_colors(7)
            characteristics = [
                localization.get("wing"),
                localization.get("antenna"),
                localization.get("caste"),
                localization.get("chitin"),
                localization.get("spirit"),
                localization.get("mandible"),
                localization.get("temperature"),
            ]
            for i in range(0, 7):
                answer += " • {0} : {1} ({2})\n".format(characteristics[i], color_to_emoji(colors[i]), color_to_characteristic_change(colors[i]))
            await message.channel.send(answer)

        elif arg.isnumeric():
            count = int(arg)
            if count < 1 or count > 42:
                await print_usage(message.channel, localization.get("invalid_count_number"))
                return

            colors = draw_colors(count)
            answer = localization.get("you_have_drawn")
            for color in colors:
                answer += " • a {0} ({1})\n".format(color_to_emoji(color), color_to_success_rate(color))
            await message.channel.send(answer)

        else:
            await print_usage(message.channel, localization.get("invalid_argument"))
            return

client.run("MTAzMDU4MDg4OTA5NDIxMzY4Mg.GAo39R.axAkfXOfv5WZTq7xdShGqjA7nbQKUPjy8VImi0")
