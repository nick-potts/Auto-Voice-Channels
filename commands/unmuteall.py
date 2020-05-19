import cfg
import discord
from functions import dm_user
from utils import log
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND>"),
        ("Description:",
         "Server unmute all users in a voice chat."),
    ]
]

async def execute(ctx, params):
    client = ctx['client']
    guild = ctx['guild']
    author = ctx['message'].author
    v = ctx['message'].author.voice

    if v is None:
        return False, "You need to be in a voice chat to use this command."
    channel = v.channel

    canMute = author.permissions_in(channel).mute_members
    if canMute != True:
        return False, "You don't have permission to server mute members"
    
    try:
        [await x.edit(mute=False) for x in channel.members]
    except discord.errors.Forbidden:
        return False, ":warning: I don't have permission to mute members :("
    except discord.errors.HTTPException as e:
        return False, ":warning: Something went wrong when trying to mute all :("

    return True, ""

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False
)
