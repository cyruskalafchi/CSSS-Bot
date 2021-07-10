# Discord Bot for UBC CSSS' Server
# bot.py

import os
import asyncio

import discord
from discord import message
from discord.user import User
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import ConversionError

import mongo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%', help_command = None, case_insensitive=True)


@bot.event
async def on_ready():
    print('Connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="%help"))


@bot.event
async def on_raw_reaction_add(payload):
    react_role = mongo.reactable_message(payload.message_id)
    react_emoji = payload.emoji.name

    if react_role != None:
        emoji_array = react_role['emojis']

        if react_emoji in emoji_array:
            role_array = react_role['roles']
            role_name = role_array[(emoji_array.index(react_emoji))]
            
            member = payload.member
            role = discord.utils.get(member.guild.roles, name=role_name)
            await member.add_roles(role)


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
    top_users = mongo.get_top_users(10)
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

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Took __**' + str(round(bot.latency, 2)) + '**__ ms to send back.')

@bot.command(name='edit')
@commands.has_role('Admin')
async def edit(ctx, user: User, points: int):
    mongo.update_points(user.id, points)
    await ctx.send('Modified ' + user.mention + '\'s points by ' + str(points))

@edit.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid input; use %edit @User points')

# @bot.command(name='reactrole add')
# @commands.has_role('Admin')
# async def edit(ctx, message: int, points: int):
#     mongo.update_points(user.id, points)
#     await ctx.send('Modified ' + user.mention + '\'s points by ' + str(points))

@bot.command(name='purge')
@commands.has_role('Admin')
async def purge(ctx, number):
    await ctx.channel.purge(limit=int(number))

@bot.command(name='help')
async def help(ctx):
   embed=discord.Embed(title="Cubey", description="A simple bot for the UBC CSSS Discord", color=0x0096ff)
   embed.add_field(name="Public Commands", value="%leaderboard \n %points \n %ping", inline=False)
   embed.add_field(name="Admin Commands", value="%edit \n %purge", inline=False)
   await ctx.send(embed=embed)

def display_points(points):
    if points > 1000:
        return str(round((points / 1000), 2)) + "k"
    else:
        return str(points)

bot.run(TOKEN)
