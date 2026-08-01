import discord
import random

from env import BOT_TOKEN, GUILD_ID

from enum import IntEnum, auto

from localization import localization_dictionnary, Language

def clamp(n, lower, upper):
    return min(max(n, lower), upper)

class Color(IntEnum):
    Black = auto()
    White = auto()
    Blue = auto()
    Green = auto()
    Red = auto()

    def __le__(self, b):
        return self.value <= b.value

def transform_color(color, bonus):
    new_color_value = color.value + bonus
    if new_color_value < Color.Black.value:
        new_color_value = Color.Black.value
    elif new_color_value > Color.Red.value:
        new_color_value = Color.Red.value
    return Color(new_color_value)

class BeetleBag:
    def __init__(self):
        self.numbers = []
        for i in range(42):
            self.numbers.append(i)

    def draw_colors(self, count):
        results = []
        for i in range(count):
            index = random.randrange(0, len(self.numbers))
            results.append(self.numbers[index])
            self.numbers.pop(index)
        colors = []
        for number in results:
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

def color_to_success_rate(color, localization):
    return str({
        Color.Black: localization.get("critical_failure"),
        Color.White: localization.get("failure"),
        Color.Blue:  localization.get("success"),
        Color.Green: localization.get("improved_success"),
        Color.Red:   localization.get("critical_success"),
    }.get(color))

def color_to_characteristic_change(color, localization):
    return str({
        Color.Black: localization.get("capacity"),
        Color.White: localization.get("1_more_skill_point"),
        Color.Blue:  localization.get("2_more_skill_point"),
        Color.Green: localization.get("1_more_skill_point_and_1_more_free_skill_point"),
        Color.Red:   localization.get("characteristic_improved"),
    }.get(color))

def color_with_bonus_str(color, bonus, localization):
    if bonus == 0:
        return "{0} ({1})\n".format(color_to_emoji(color), color_to_success_rate(color, localization))
    final_color = transform_color(color, bonus)
    return "{0} -> {1} ({2})\n".format(color_to_emoji(color), color_to_emoji(final_color), color_to_success_rate(final_color, localization))

def list_colors_with_bonus(colors, bonus, localization):
    answer = localization.get("you_have_drawn")
    for color in colors:
        answer += " • {0}".format(color_with_bonus_str(color, bonus, localization))
    return answer


intents = discord.Intents.default()

class Insectobot(discord.Client):

    def __init__(self):
        super().__init__(intents=intents)
        self.localization = localization_dictionnary()
        self.tree = discord.app_commands.CommandTree(self)


        @self.tree.command(name = "language", description = "Change language", guild=discord.Object(id=GUILD_ID))
        async def command_language(interaction: discord.Interaction, language: str):
            language = language.lower()
            languages = {
                "french": Language.French,
                "français": Language.French,
                "english": Language.English,
                "anglais": Language.English,
            }
            if not language in languages:
                await interaction.response.send_message(self.localization.get("invalid_language"))
                return
            self.localization.set_language(languages.get(language))
            await interaction.response.send_message(self.localization.get("language_set"))

        @self.tree.command(name = "born", description = "draw 7 beetles for character creation.", guild=discord.Object(id=GUILD_ID))
        async def command_born(interaction: discord.Interaction):
            answer = self.localization.get("you_have_drawn")
            colors = BeetleBag().draw_colors(7)
            characteristics = [
                self.localization.get("wing"),
                self.localization.get("antenna"),
                self.localization.get("caste"),
                self.localization.get("chitin"),
                self.localization.get("spirit"),
                self.localization.get("mandible"),
                self.localization.get("temperature"),
            ]
            for i in range(0, 7):
                answer += " • {0} : {1} ({2})\n".format(characteristics[i], color_to_emoji(colors[i]), color_to_characteristic_change(colors[i], self.localization))
            await interaction.response.send_message(answer)

        @self.tree.command(name = "draw", description = "directly draw N beetles.", guild=discord.Object(id=GUILD_ID))
        async def command_draw(interaction: discord.Interaction, count: int, bonus: int = 0):
            if count < 1 or count > 42:
                await interaction.response.send_message(self.localization.get("invalid_count_number"))
                return
            if bonus < -2 or bonus > 2:
                await interaction.response.send_message(self.localization.get("invalid_bonus"))
                return
            colors = BeetleBag().draw_colors(count)
            answer = list_colors_with_bonus(colors, bonus, self.localization)
            await self.answer_checked_length(interaction, answer)

        @self.tree.command(name = "skill", description = "Skill test for given difficulty", guild=discord.Object(id=GUILD_ID))
        async def command_skill(interaction: discord.Interaction, skill: int, difficulty: int, bonus: int = 0):
            difference = difficulty - skill
            difference = clamp(difference, -42, 42)
            answer = ""
            if difference <= -2:
                colors = BeetleBag().draw_colors(-difference)
                answer = list_colors_with_bonus(colors, bonus, self.localization)
                final_color = transform_color(max(colors), bonus)
                answer += "{0}: {1} ({2})".format(self.localization.get("result"), color_to_emoji(final_color), color_to_success_rate(final_color, self.localization))
            elif difference == -1:
                bag = BeetleBag()
                color = bag.draw_colors(1)[0]
                answer = self.localization.get("you_have_drawn")
                answer += color_with_bonus_str(color, bonus, self.localization)
                if transform_color(color, bonus) <= Color.White:
                    answer += self.localization.get("redraw")
                    answer += color_with_bonus_str(bag.draw_colors(1)[0], bonus, self.localization)
            elif difference == 0:
                bag = BeetleBag()
                color = bag.draw_colors(1)[0]
                answer = self.localization.get("you_have_drawn")
                answer += color_with_bonus_str(color, bonus, self.localization)
            elif difference == 1:
                bag = BeetleBag()
                color = bag.draw_colors(1)[0]
                answer = self.localization.get("you_have_drawn")
                answer += color_with_bonus_str(color, bonus, self.localization)
                if transform_color(color, bonus) > Color.White:
                    answer += self.localization.get("redraw")
                    answer += color_with_bonus_str(bag.draw_colors(1)[0], bonus, self.localization)
            else:
                colors = BeetleBag().draw_colors(difference)
                answer = list_colors_with_bonus(colors, bonus, self.localization)
                final_color = transform_color(min(colors), bonus)
                answer += "{0}: {1} ({2})".format(self.localization.get("result"), color_to_emoji(final_color), color_to_success_rate(final_color, self.localization))

            await self.answer_checked_length(interaction, answer)

        @self.event
        async def on_ready():
            await self.tree.sync(guild=discord.Object(id=GUILD_ID))
            print("We have logged in as {0.user}".format(client))

    async def answer_checked_length(self, interaction: discord.Interaction, answer: str):
        if len(answer) >= 2000:
            await interaction.response.send_message(self.localization.get("too_long_answer"))
        else:
            await interaction.response.send_message(answer)

client = Insectobot()
client.run(BOT_TOKEN)
