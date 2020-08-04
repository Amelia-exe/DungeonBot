import os
import discord
import asyncio
from discord import Embed
from discord import Colour
from discord.ext import commands
from dotenv import load_dotenv

from cmds.help_command import HelpCommand
from helpers import fuzzle as fuzzle

load_dotenv()
PFX = os.getenv('PREFIX')

class Dmaster(commands.Bot):
    def __init__(self, **options):
        super().__init__(PFX, case_insensitive=True, help_command=HelpCommand(),
                         description="The only DungeonMaster you'll ever need.", **options)

    @property
    def embed(self):
        embed = Embed(colour=Colour.red())
        embed.set_footer(text=f"DungeonBot by Amelia",
                         icon_url=self.user.avatar_url)
        return embed

    # Command removal line, can be used in any Cog to remove commands used.
    @staticmethod
    async def auto_delete(ctx: commands.Context):
        if not getattr(ctx.message.flags, "command_removal", False):
            await ctx.message.delete(delay=2.0)

    async def on_command_error(self, ctx: commands.Context, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            await self.auto_delete(ctx)
            cmds = [{"key": cmd.name, "tags": cmd.aliases, "cmd": cmd} for cmd in ctx.bot.commands]
            results = fuzzle.find(cmds, ctx.message.content, 0.02)
            if results:
                top_cmds = '\n'.join([f"`{self.get_cmd_string(cmd['cmd'])}`" for cmd in results][:3])
                await ctx.send(f"No command called \"{ctx.message.content}\" found. " +
                                                f"Maybe you meant?\n\n{top_cmds}\n\n" +
                                                "Powered by Fuzzle™.")
            else:
                await ctx.send(f"No command called \"{ctx.message.content}\" found. Please try a different search.")
            return
        elif isinstance(error, commands.CheckFailure):
            await self.auto_delete(ctx)
            await ctx.send(f'You do not have access to: **{PFX}{ctx.message}**." \
                "If you believe this to be wrong, contact an administrator.', delete_after=30)
            return
        raise error

    # Allows the user to know the bot has loaded successfully.
    async def on_ready(self):
        print(
            f"User: {self.user} | ID: {self.user.id}, has completed connecting to Discord.")

bot = Dmaster()
# Connects the Addons to the index bot page, allowing commands to be used.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename.startswith('__init__'):
            print("__init__ was ignored.")
            continue
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Extension: {filename[:-3]} has been initialised.')

async def run():
    await bot.start(str(os.getenv('TOKEN')))

async def logout():
    print(f"User: {bot.user} | ID: {bot.user.id}, has been shut down.")
    await bot.logout()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    loop.close()
finally:
    loop.close()