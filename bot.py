# Discord Bot for UBC CSSS' Server
# bot.py
import os
import asyncio

import discord
from discord import message
from discord.flags import Intents
from discord.user import User
from discord.ext import commands
from discord.ext.commands import ConversionError

from dotenv import load_dotenv
from db import mongo

from core import cubey_points
from core import react_roles
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='%', help_command=None, case_insensitive=True, intents=intents)

# ======== Miscellanous Functions ========
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

@bot.command(name='help')
async def help(ctx):
   embed=discord.Embed(title="Cubey", description="A simple bot for the UBC CSSS Discord", color=0x0096ff)
   embed.add_field(name="Public Commands", value="%leaderboard \n %points \n %ping", inline=False)
   embed.add_field(name="Admin Commands", value="%edit \n %purge", inline=False)
   await ctx.send(embed=embed)


# ======== React Role Functions ========
@bot.event
async def on_raw_reaction_add(payload):
    react_check = react_roles.check_role(payload, bot)
    
    if react_check:
        member, role = react_check
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    react_check = react_roles.check_role(payload, bot)
    
    if react_check:
        member, role = react_check
        await member.remove_roles(role)

@bot.event
async def on_raw_message_delete(payload):
    react_roles.delete_react_role(payload)

# ======== Point Functions ========
@bot.command(name='points')
async def points(ctx):
    await ctx.send(cubey_points.user_points(ctx))

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    await ctx.send(embed=cubey_points.leaderboard(ctx))

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Took __**' + str(round(bot.latency * 1000, 2)) + '**__ ms to send back.')

@bot.command(name='edit')
@commands.has_role('Admin')
async def edit(ctx, user: User, points: int):
    await ctx.send(cubey_points.edit_points(ctx, user, points))

@edit.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid input; use %edit @User points')


# ======== Moderation Functions ========
@bot.command(name='purge')
@commands.has_role('Admin')
async def purge(ctx, number):
    await ctx.channel.purge(limit=int(number))

@bot.command(name='selfpurge')
async def purge(ctx, number):
    await ctx.channel.purge(limit=int(number)+1, check=lambda message: message.author == ctx.author)

bot.run(TOKEN)
