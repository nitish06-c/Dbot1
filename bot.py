import discord
from discord.ext import commands
import random
from discord.ext import tasks
from itertools import cycle
import os
import json
import asyncio
from discord import Spotify


description = '''Bot for server moderation and fun activities.'''

bot = commands.Bot(command_prefix = '.', description = description)
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@bot.event
async def on_ready():
    print('Logged in as 8ball bot')
    print(bot.user.name)
    print(bot.user.id)
    print('User is Online')


@bot.command()
async def hi(ctx):
    await ctx.send(f'Hi i am {ctx.user}')


@bot.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command Used')

@bot.command(aliases = ['quote'])
async def quote_himym(ctx):
    quotes = ["Whenever I’m sad, I stop being sad and be awesome instead — Barney Stinson",
              "We struggle so hard to hold on to these things that we know are gonna disappear eventually. And that’s really noble — Lily Aldrin",
              "Because sometimes even if you know how something’s gonna end, that doesn’t mean you can’t enjoy the ride — Ted Mosby",
              "That’s life, you know. We never end up where you thought you wanted to be — Marshall Eriksen",
              "Oh my god, look at you cowards. So afraid of any kind of change. So terrified of anything new. So, so desperate to cling to anything comfortable and familiar — Robin Scherbatsky",
              "We’re going to get older, whether we like it or not, so the only question is whether we get on with our lives or desperately cling to the past — Ted Mosby",
              "I wound up shame-eating the whole pizza. I woke up all greasy and sweaty. My sheets looked like what they wrap deli sandwiches in. Maybe I should join a gym. Do you go to a gym? — Ted Mosby",
              "Look, you can’t design your life like a building. It doesn’t work that way. You just have to live it, and it’ll design itself — Lily Aldrin",
              "You can’t just skip ahead to where you think your life should be — Lily Aldrin",
              "It’s just, eventually we’re all gonna move on. It’s called growing up — Lily Aldrin",
              "There are two big days in any love story: the day you meet the girl of your dreams and the day you marry her — Ted Mosby",
              "Guys are like the subway. You miss one, another comes along in five minutes.” “Unless it’s the end of the night, and then you get on anything — Robin Scherbatsky/Lily Aldrin",
              "A word of advice: Play along. The more you fight it, the worse it’s gonna get. It’s like when your car slides on ice, you steer into the skid — Ted Mosby" ]
    await ctx.send(f'Your Quote for the day : {random.choice(quotes)}')

def is_it_me(ctx):
    return ctx.author.id == 120893635016392704

@bot.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi im {ctx.author}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@bot.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don’t count on it.',
                 'It is certain.',
                 'It is decidedly so.',
                 'Most likely.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Outlook good.',
                 'Reply hazy, try again.',
                 'Signs point to yes.',
                 'Very doubtful.',
                 'Without a doubt.',
                 'Yes.',
                 'Yes – definitely.',
                 'You may rely on it.']
    await ctx.send(f'Question: {question}\nAnswer = {random.choice(responses)}')
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

@bot.command()
async def bleh(ctx):
    await ctx.send('shit!', delete_after=2)


@bot.command()
async def spotify(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            await ctx.send(f"{user} is listening to {activity.title} by {activity.artist}")

bot.run('NzIzOTU2OTI0MDkzMzAwODQ3.XvT5lQ.LjPqcbA82iNKYmWLBbf8I64GUP8')


