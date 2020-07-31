import datetime
import operator
import random
from enum import Enum

from discord import Color, Embed


class EmbedColor(Enum):

    BLUE = Color(0x004080)
    DARK_BLUE = Color(0x004080)
    NAVY_BLUE = Color(0x000040)
    TEAL = Color(0x008080)
    ORANGE = Color(0xff8040)
    RED = Color(0xff0000)
    WINE_RED = Color(0x804040)
    MAROON = Color(0x400000)
    GREEN = Color(0x004000)
    TURQUOISE = Color(0x008080)
    PURPLE = Color(0x8000ff)
    PINK = Color(0xff00ff)
    DARK_PINK = Color(0x800040)

    def __index__(self):
        return operator.index(self.value.value)


# TODO: Make use of embed template in bot
class EmbedBuilder:

    ICON_URL = "https://i.imgur.com/IdEAN1j.jpg"

    # TODO: Finish mypy typing
    # TODO: Use timestamp
    @classmethod
    def make_embed(cls, title: str, desc: str, author=None, fields=None, footer=None,
                   url=None, timestamp=None, empty_field=False):
        # TODO: Fix `NoneType` check
        embed = discord.Embed(
            title=title,
            description=desc,
            color=random.choice([c for c in EmbedColor]).value,
            url=url)

        if author:
            embed.set_author(name=author["name"], icon_url=author["icon_url"])

        if fields:
            for field in fields:
                name = field[0]
                value = field[1]

                if empty_field:
                    if not name:
                        name = "\u200b"
                    if not value:
                        value = "\u200b"

                inline = field[2]
                if not inline:
                    inline = True
                if name and value:
                    embed.add_field(name=name, value=value, inline=inline)
        if not footer:
            footer = ">>> Please donate to keep me alive <<<"
        embed.set_footer(text=footer, icon_url=cls.ICON_URL)
        return embed
