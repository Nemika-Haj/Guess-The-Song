import discord

from core.database import Levels as leveldb
from core import embeds, files

from textwrap import dedent

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
            title=f"{user.name} | Level Info",
            description=dedent(f"""◽ **Level ➜** {profile['level']}
            ◽ **Experience ➜** {profile['xp']}
            ◽ **Needed ➜** {profile['level']*3-profile['xp']}
            
            *Check out the **[Dashboard]({files.Data('config').yaml_read()['dashURL']})** for all the global leaderboard!*"""),
            color=discord.Color.red()
        )
        .set_thumbnail(url=user.avatar_url_as(static_format="png")))

def setup(bot):
    bot.add_cog(Levels(bot))
    
    