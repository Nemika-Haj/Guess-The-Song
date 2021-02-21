import discord, youtube_dl, asyncio, json, random, os

from youtube_search import YoutubeSearch

from core import checks, embeds, files, database

from discord.ext import tasks

from difflib import SequenceMatcher

commands = discord.ext.commands

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing = []

    def similar(self, s_1, s_2): return SequenceMatcher(None, s_1, s_2).ratio() > 0.6

    @commands.guild_only()
    @commands.command()
    async def play(self, ctx, *, category="random"):
        if not ctx.author.voice: return
        if ctx.author.voice in self.playing: return await ctx.send(embed=embeds.Embeds("Already playing!").error())

        categories = [i[:-5] for i in os.listdir("data") if i.endswith(".json")]

        if not category.lower() in categories: return await ctx.send(embed=embeds.Embeds("There's no such category! The available categories are; " + ','.join(f"`{i}`" for i in categories)).error())

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        song = random.choice(files.Data(category).json_read())

        player = await YTDLSource.from_url(song, loop=self.bot.loop)

        title = player.title.lower()

        ctx.voice_client.play(player)

        await ctx.send(embed=discord.Embed(
            title="Guess The Song!",
            description=f"Now playing track! Try to guess the song before it's over!\n*`Mode: {category}`*",
            color=discord.Color.green()
        ))

        self.playing.append(ctx.author.voice)

        try:
            answer = await self.bot.wait_for(
                "message",
                timeout=player.data['duration'],
                check=lambda message: self.similar(message.content.lower(), title) or (message.content.lower() == "forcestop" and message.author.id == ctx.author.id)
            )

        except asyncio.TimeoutError:
            self.playing.remove(ctx.author.voice)
            await ctx.voice_client.disconnect()
            return await ctx.send(embed=discord.Embed(
                title="Song is over!",
                description=f"Nobody guessed the song! It was `{player.title}`!",
                color=discord.Color.red(),
                url=player.data['webpage_url']
            )
            .set_thumbnail(url=player.data['thumbnail']))

        if answer.content.lower() == "forcestop":
            self.playing.remove(ctx.author.voice)
            await ctx.voice_client.disconnect()
            return await ctx.send(embed=discord.Embed(
                title="Force Stop!",
                description=f"The song was force stopped! It was `{player.title}`!",
                color=discord.Color.red(),
                url=player.data['webpage_url']
            )
            .set_thumbnail(url=player.data['thumbnail']))

        database.Levels(answer.author.id).add_xp()
        self.playing.remove(ctx.author.voice)
        return await ctx.send(embed=discord.Embed(
                title="Congratulations!",
                description=f"{answer.author.mention} guessed the song! It was `{player.title}`!",
                color=discord.Color.green(),
                url=player.data['webpage_url']
            )
            .set_thumbnail(url=player.data['thumbnail']))
    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if not ctx.voice_client:
            if not ctx.author.voice:
                return await ctx.send(embed=embeds.Embeds("You must be connected in a voice channel!").error())
            else:
                await ctx.author.voice.channel.connect()


def setup(bot):
    bot.add_cog(Music(bot))