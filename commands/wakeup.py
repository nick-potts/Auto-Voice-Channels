import cfg
import discord
from functions import dm_user
from utils import log
from commands.base import Cmd
import asyncio

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> userid"),
        ("Description:",
         "Moves a user around until they undeafen"),
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
    try:
        name = int(name)
    except ValueError:
        return False, ("`{}` is not a valid user id".format(name))

    user = next((member for member in oldChannel.members if member.id == int(name)), None)
    if user is None:
        return False, "The user must be in your voice channel."

    perms = {
        guild.default_role: discord.PermissionOverwrite(connect = False, view_channel = True),
        guild.me: discord.PermissionOverwrite(manage_channels=True, connect=True, move_members=True)
    }
    vc1 = await guild.create_voice_channel("boing", overwrites=perms)
    vc2 = await guild.create_voice_channel("bounce", overwrites=perms)

    try:
        while user.voice is not None and user.voice.self_deaf:
            await user.move_to(vc1)
            await asyncio.sleep(1)
            await user.move_to(vc2)
            await asyncio.sleep(1)
    except:
        #clean up
        va = True
    
    try:
        await user.move_to(oldChannel)
    except:
        #clean up
        va = True
    try:
        await vc1.delete()
        await vc2.delete()
    except:
        va=True
    
    
    # canJoin = author.permissions_in(newChannel).connect
    # if canJoin != True:
    #     return False, "You don't have permissions to join that channel"

    # try:
    #     [await x.move_to(newChannel) for x in oldChannel.members]
    # except discord.errors.Forbidden:
    #     return False, ":warning: I don't have permission to move all to **{}** :(".format(newChannel.name)
    # except discord.errors.HTTPException as e:
    #     return False, ":warning: Something went wrong when trying to move all to **{}** :(".format(newChannel.name)

    return True, "Success, they have been awoken"

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=True
)