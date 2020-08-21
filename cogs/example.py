import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client


    #commands

    @commands.command()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid Command Used')
def setup(client):
    client.add_cog(Example(client))

