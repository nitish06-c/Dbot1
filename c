@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


   def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

 @client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to {prefix}')


    youtube_dl.utils.bugs_report_message = lambda: ''





ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
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
    async def from_url(cls, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None,lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect
    @commands.command()
    async def play(self, ctx, *, query):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'. format(query))
    @commands.command()
    async def yt(self, ctx, *, url):

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'. format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))
    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not Connected To A Voice Channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed Volume to {}%".format(volume))
    @commands.command()
    async def stop(self, ctx):

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot.add_cog(Music(bot))


@bot.command(aliases = ['movies thriller'])
async def movies_thriller(ctx):
    thriller = ["Se7en (1995 Dir.David Fincher) - Brad Pitt, Morgan Freeman",
                "The Prestige (2006 Dir. Christopher Nolan) - Christian Bale, Hugh Jackman",
                "Psycho (1960 Dir. Alfred Hitchcock) - Anthony Perkins, Janet Leigh",
                "The Silence of the Lambs (1991 Dir. Jonathan Demme) - Jodie Foster, Anthony Hopkins",
                "Rope (1948 Dir. Alfred Hitchcock) - James Stewart, Farley Granger",
                "Chinatown (1974 Dir. Roman Polanski) - Jack Nicholson, Roman Polanski",
                "Memento (2000 Dir. Christopher Nolan) - Guy Pearce, Carie-Anne Moss",
                "The Departed (2006 Dir. Martin Scorcese) - Leonardo Dicaprio, Matt Damon",
                "Taxi Driver (1976 Dir. Martin Scorcese) - Robert De Niro, Harvey Keitel",
                "Inception (2010 Dir. Christopher Nolan) - Leonardo Dicaprio, Tom Hardy, Joseph Gordon-Lewitt",
                "Fight Club (1999 Dir. David Fincher) - Brad Pitt, Edward Norton, Helena Bonham Carter"]

    await ctx.send(f'Genre : Thriller\nMovie : {random.choice(thriller)}')

@bot.command()
async def movies_crime(ctx):
    crime = ["Goodfellas (1990 Dir. Martin Scorcese) - Ray Liotta, Robert De Niro, Joe Pesci",
             "Godfather (1972 Dir. Francis Ford Coppola) - Al Pacino, Marlon Brando,",
             "Pulp Fiction (1994 Dir. Quentin Tarantino) - Samuel L Jackson, John Travolta",
             "Casino (1994 Dir. Martin Scorcese) - Robert De Niro, Joe Pesci, Sharon Stone",
             "Reservoir Dogs (1992 Dir. Quentin Tarantino) - Quentin Tarantino, Harvey Keitel",
             "Scarface (1983 Dir. Brian De Palma) - Al Pacino, Michelle Pfeifer",
             "Heat (1995 Dir. Michael Mann) - Robert De Niro, Al Pacino"]
    await ctx.send(f'Genre : Crime\nMovie : {random.choice(crime)}')

@bot.command()
async def movies_comedy(ctx):
    comedy = ['The Hangover (2008 Dir. Todd Philips) - Bradley Cooper, Jack Gallifiankis',
              "Borat: Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan’ (2006 Dir. Larry Charles) - Sacha Baron Cohen",
              "Superbad (2007 Dir. Greg Mottola) - Jonah Hill, Seth Rogen"]
    await ctx.send(f'Genre : Comedy\nMovie : {random.choice(comedy)}')