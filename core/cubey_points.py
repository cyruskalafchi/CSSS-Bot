from db import mongo
import discord

# Context -> String
# Finds users points and returns it as a string
def user_points(ctx):
    raw_points = mongo.find_points(ctx.author.id)
    converted_points = convert_points_to_str(raw_points)
    message = ctx.author.mention + ", you have " + converted_points + " points!"
    return message

# [Context, User, Integer] -> String
# Updates given user's points by given integer amount and returns confirmation message
def edit_points(ctx, user, points):
    mongo.update_points(user.id, points)
    message = 'Modified ' + user.mention + '\'s points by ' + convert_points_to_str(points)
    return message

# Context -> Embed
# Builds and returns leaderboard embed based on top points in DB 
def leaderboard(ctx):
    top_users = mongo.get_top_users(10)
    output = ""
    count = 1

    for user in top_users:
        output = output + str(count) + ": <@" + str(user['id']) + "> (" + convert_points_to_str(user['points']) + ") \n"
        count += 1

    if len(output) < 1:
        output = "Sorry, the leaderboard appears to be empty!"
    
    embed = discord.Embed(color=0x0096ff)
    embed.add_field(name="Leaderboard", value=output, inline=False)
    
    return embed

# Integer -> String
# Converts and returns integers into string displayed in thousands (xxk points)
def convert_points_to_str(points):
    if points > 1000:
        return str(round((points / 1000), 2)) + "k"

    return str(points)