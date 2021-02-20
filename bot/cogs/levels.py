import discord

from core.database import Levels as leveldb
from core import embeds

commands = discord.ext.commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.command()
    async def level(self, ctx, user:discord.User=None):
        if not user: user = ctx.author

        db = leveldb(user.id)
        profile = db.get()

        return await ctx.send(embed=discord.Embed(
            title="Level Profile!",
            description=f"You are currently Level {profile['level']} with {profile['exp']} experience",
            color=discord.Color.green()
        ))

def setup(bot):
    bot.add_cog(Levels(bot))
    
    