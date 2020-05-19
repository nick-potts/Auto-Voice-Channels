import cfg
import discord
from functions import dm_user
from utils import log
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> channel"),
        ("Description:",
         "Move all users in one voice chat to another voice chat. You can specify either the name or the ID."),
    ]
]

async def execute(ctx, params):
    client = ctx['client']
    guild = ctx['guild']
    author = ctx['message'].author
    v = ctx['message'].author.voice
    if v is None:
        return False, "You need to be in a voice chat to use this command."
    oldChannel = v.channel
    
    name = ' '.join(params).strip()
    newChannel = discord.utils.get(guild.voice_channels, name=name)
    if newChannel is None:
        try:
            name = int(name)
        except ValueError:
            return False, ("Failed to find channel with name `{}`".format(name))
        newChannel = client.get_channel(int(name))
        if newChannel is None:
            return False, "Failed to find channel with id `{}`".format(name)

    canJoin = author.permissions_in(newChannel).connect
    if canJoin != True:
        return False, "You don't have permissions to join that channel"

    try:
        [await x.move_to(newChannel) for x in oldChannel.members]
    except discord.errors.Forbidden:
        return False, ":warning: I don't have permission to move all to **{}** :(".format(newChannel.name)
    except discord.errors.HTTPException as e:
        return False, ":warning: Something went wrong when trying to move all to **{}** :(".format(newChannel.name)

    return True, ""

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=True
)
