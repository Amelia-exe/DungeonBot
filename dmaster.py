import discord, os
from discord.ext import commands
import configparser

# Enables getting the prefix, client_id and bot token from file
config= configparser.ConfigParser()
config.read("config.ini")
pfx= config["TDM"]["prefix"]

class DungeonMaster(commands.Bot):
    def __init__(self, **options):
        super().__init__(
            pfx,
            description="The only DungeonMaster you'll ever need.",
            **options)

    # Command removal line, can be used in any Cog to remove commands used.
    async def slim_delete(self, ctx: commands.Context):
        if not getattr(ctx.message.flags, "command_removal", False):
            await ctx.message.delete(delay=1.8)

    # Generic error handler, for when a specific handler is not present to catch errors.
    # Removes commands entered and throws/catches errors. Else, prints to console.
    async def on_command_error(self, ctx: commands.Context, error):
        #Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            await self.slim_delete(ctx)
            await ctx.send(f'**{pfx}{ctx.message}** is not a valid input. Please check the command usage and try again. <@{ctx.message.author.id}>', delete_after=30)
        elif isinstance(error, commands.CheckFailure):
            await self.slim_delete(ctx)
            await ctx.send(f'You do not have access to: **{pfx}{ctx.message}**. If you believe this to be wrong, contact an administrator.', delete_after=30)
            return
        raise error

bot = DungeonMaster()

@bot.event
async def on_ready():
    print(f'{bot.user} has completed connecting to Discord.')

# Connects the Extensions to the dmaster bot, allowing commands to be used.
for filename in os.listdir('./cog'):
    if filename.endswith('.py'):
        if filename.startswith('__init__'):
            print("__init__ was ignored.")
            continue
        bot.load_extension(f'cog.{filename[:-3]}')
        print(f'Extension: {filename[:-3]} has been initalised.')

bot.run(config["TDM"]["client_token"])