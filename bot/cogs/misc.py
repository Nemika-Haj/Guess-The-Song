import discord, datetime

from textwrap import dedent

from core import files, embeds

commands = discord.ext.commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):
        return await ctx.send(embed=embeds.Embeds(f"Pong! `{round(self.bot.latency*1000)}ms`!").success())

    @commands.guild_only()
    @commands.command(aliases=["info"])
    async def help(self, ctx):
        config = files.Data("config").yaml_read()

        owners = ', '.join([str(await self.bot.fetch_user(i)) for i in config['managers']])

        uptime = (datetime.datetime.now() - self.bot.startTime).seconds

        hours = uptime//3600
        uptime %= 3600
        minutes = uptime//60
        seconds = uptime % 60

        uptime = (f"{hours} hours " if hours else "") + (f"{minutes} minutes " if minutes else "") + f"{seconds} seconds"

        return await ctx.send(embed=discord.Embed(
            title=f"{self.bot.user.name} | Help",
            description=dedent(f"""Can you guess songs? Are you sure? Prove it! Use `{config['prefix']}play` and put your song-guessing skills to the test!
            
            > **Uptime:** {uptime}
            > **Version:** {config['version']}
            > **Library:** Discord.py {discord.__version__}
            > **Owners:** {owners}"""),
            color=discord.Color.blurple()
        )
        .set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png")))

def setup(bot):
    bot.add_cog(Misc(bot))