# Discord Bot for UBC CSSS' Server
# bot.py

import os
import discord
from discord import message
from discord.user import User
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import ConversionError

import mongo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%', help_command = None)


@bot.event
async def on_ready():
    print('Connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="%help"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user = message.author.id
    mongo.update_points(user, len(message.content))

    await bot.process_commands(message)

@bot.command(name='points')
async def points(ctx):
    user_points = mongo.find_points(ctx.author.id)
    await ctx.send(ctx.author.mention + ", you have " + display_points(user_points) + " points!")

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    top_users = mongo.get_top_users(5)
    output = ""
    count = 1

    for user in top_users:
        output = output + str(count) + ": <@" + str(user['id']) + "> (" + display_points(user['points']) + ") \n"
        count += 1

    if len(output) < 1:
        output = "Sorry, the leaderboard appears to be empty!"
    
    embed=discord.Embed(color=0x0096ff)
    embed.add_field(name="Leaderboard", value=output, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='edit')
@commands.has_role('Admin')
async def edit(ctx, user: User, points: int):
    mongo.update_points(user.id, points)
    await ctx.send('Modified ' + user.mention + '\'s points by ' + str(points))

@edit.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid input; use %edit @User points')

@bot.command(name="help")
async def help(ctx):
   embed=discord.Embed(title="Cubey", description="A simple bot for the UBC CSSS Discord", color=0x0096ff)
   embed.add_field(name="Commands", value="%leaderboard \n %points", inline=False)
   await ctx.send(embed=embed)

def display_points(points):
    if points > 1000:
        return str(round((points / 1000), 2)) + "k"
    else:
        return str(points)

bot.run(TOKEN)
