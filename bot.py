# Discord Bot for UBC CSSS' Server
# bot.py

import os
import discord
from discord import message
from discord.user import User
from dotenv import load_dotenv
from discord.ext import commands

import database

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%', help_command = None)
connection = database.connect()
database.create_tables(connection)

@bot.event
async def on_ready():
    print('Connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="%help"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user = message.author.id
    user_userpoint = database.get_userpoints_by_user(connection, message.author.id)

    if (user_userpoint == None):
        database.add_userpoints(connection, user, 0)
    else:
        add_points(user_userpoint, len(message.content))

    await bot.process_commands(message)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    top_users = database.get_top_users(connection)
    output = ""
    count = 1

    for user in top_users:
        output = output + str(count) + ": <@" + str(user[1]) + "> (" + display_points(user[2]) + ") \n"
        count += 1

    if len(output) < 1:
        output = "Sorry, the leaderboard appears to be empty!"
    
    embed=discord.Embed(color=0x0096ff)
    embed.add_field(name="Leaderboard", value=output, inline=False)
    await ctx.send(embed=embed)
    
    
@bot.command(name='points')
async def points(ctx):
    user_userpoint = database.get_userpoints_by_user(connection, ctx.author.id)
    await ctx.send(ctx.author.mention + ", you have " + display_points(user_userpoint[2]) + " points!")

@bot.command(name="help")
async def help(ctx):
   embed=discord.Embed(title="Cubey", description="A simple bot for the UBC CSSS Discord", color=0x0096ff)
   embed.add_field(name="Commands", value="%leaderboard \n %points", inline=False)
   await ctx.send(embed=embed)

@bot.command(name='edit')
@commands.has_role('Admin')
async def edit(ctx, user: User, points: int):
    try:
        add_points(database.get_userpoints_by_user(connection, user.id), points)
        await ctx.send('Modified ' + user.mention + '\'s points by ' + str(points))

    except:
        await ctx.send('Invalid input; use %edit @User points')

def add_points(user, points):
    database.update_userpoints(connection, user[2] + points, user[1])

def display_points(points):
    if points > 1000:
        return str(round((points / 1000), 2)) + "k"
    else:
        return str(points)

bot.run(TOKEN)
