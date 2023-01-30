import discord

import sys
import socket

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

import logging


import datetime

import db

import secrets

intents = discord.Intents.all()


client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_message(message):
    member = message.author
    member_id = str(message.author.id)

    if message.author == client.user:
        return

    db.insert_user(member_id)

    if message.content.startswith('!start'):
        db.add_task(member_id, "start")
        await DM(member, "Started session")

    if message.content.startswith('!tokens'):
        tokens = db.get_tokens(member_id)[0]
        await DM(member, f"You have {tokens} tokens")

    #TODO include payment
    if message.content.startswith('!charge'):
        db.increase_tokens(member_id, 1)
        tokens = db.get_tokens(member_id)
        await DM(member, f"You have {tokens} tokens")

    if message.content.startswith('!stop'):
        db.add_task(member_id, "stop")
        await DM(member, f"Stopped your session")

    if message.content.startswith('!queue'):
        await DM(member, f"Your queue: {str(db.get_tasks())}")


async def DM(member: discord.Member, message):
    channel = await member.create_dm()
    await channel.send(message)


if __name__ == '__main__':
    client.run(secrets.discord_token)


