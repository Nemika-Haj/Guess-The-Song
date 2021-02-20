import discord
from ..core.database import Levels as leveldb

commands = discord.ext.commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_commands=True)
    async def level(self, ctx):
        db = leveldb(ctx.author.id)
        profile = db.get
        await ctx.send(embed=discord.Embed(
            title="Level Profile!",
            description=f"You are currently Level {profile.level} with {profile.xp} experience",
            color=discord.Color.green()
        ))
    
    