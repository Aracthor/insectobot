import discord
import random

from env import BOT_TOKEN, GUILD_ID

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
tree = discord.app_commands.CommandTree(client)

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


@tree.command(name = "language", description = "Change language", guild=discord.Object(id=GUILD_ID))
async def command_language(interaction: discord.Interaction, language: str):
    language = language.lower()
    languages = {
        "french": Language.French,
        "français": Language.French,
        "english": Language.English,
        "anglais": Language.English,
    }
    if not language in languages:
        await interaction.response.send_message(localization.get("invalid_language"))
        return
    localization.set_language(languages.get(language))
    await interaction.response.send_message(localization.get("language_set"))

@tree.command(name = "born", description = "draw 7 beetles for character creation.", guild=discord.Object(id=GUILD_ID))
async def command_born(interaction: discord.Interaction):
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
    await interaction.response.send_message(answer)

@tree.command(name = "draw", description = "draw N beetles for any game test.", guild=discord.Object(id=GUILD_ID))
async def command_draw(interaction: discord.Interaction, count: int):
    if count < 1 or count > 42:
        await interaction.response.send_message(localization.get("invalid_count_number"))
        return

    colors = draw_colors(count)
    answer = localization.get("you_have_drawn")
    for color in colors:
        answer += " • {0} ({1})\n".format(color_to_emoji(color), color_to_success_rate(color))
    await interaction.response.send_message(answer)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("We have logged in as {0.user}".format(client))


client.run(BOT_TOKEN)
