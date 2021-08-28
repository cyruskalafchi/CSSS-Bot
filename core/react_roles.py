from db import mongo
import discord
import asyncio

# [Payload, Bot] -> [Member, Role] or False
# Checks if message has react role and returns Member and role if found
# Returns False if no react role found
def check_role(payload, bot):
    # On message react, get react role data from DB
    react_role = mongo.reactable_message(payload.message_id)
    react_emoji = payload.emoji.name

    if react_role != None:
        emoji_array = react_role['emojis']

        if react_emoji in emoji_array:
            # Assign role at corresponding emoji's index
            role_array = react_role['roles']
            role_name = role_array[(emoji_array.index(react_emoji))]
            
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(member.guild.roles, name=role_name)
            return [member, role]

# Payload -> None
# Deletes react role entry from DB once corresponding message has been deleted
def delete_react_role(payload):
    deleted_react_role = mongo.reactable_message(payload.message_id)

    if deleted_react_role != None:
        mongo.delete_react_role(deleted_react_role)
