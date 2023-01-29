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

db.db_action("CREATE TABLE IF NOT EXISTS users(username text, email text)")
print(db.db_action("SELECT count(*) FROM users")[0][0])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    member = message.author
    member_id = str(message.author.id)

    if message.author == client.user:
        return


    #TODO doesnt work
    logging.basicConfig(filename='discord.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug("Message: " + message.content + " | Author: " + str(message.author) + " | Time: " + str(datetime.datetime.now()))

    db.insert_user(member_id)

    if message.content.startswith('!start'):
        await start_session(member_id)

    if message.content.startswith('!tokens'):
        tokens = db.get_tokens(member_id)
        await DM(member, f"You have {tokens} tokens")

    #TODO include payment
    if message.content.startswith('!charge'):
        db.increase_tokens(member_id, 1)
        tokens = db.get_tokens(member_id)
        await DM(member, f"You have {tokens} tokens")

    if message.content.startswith('!stop'):
        db.add_task(member_id, "stop")
        await DM(member, f"Stopped your session")


async def DM(member: discord.Member, message):
    channel = await member.create_dm()
    await channel.send(message)

async def start_session(member_id):
    db.add_task(member_id, "start")
    tokens = db.get_tokens(member_id)
    if tokens:
        db.decrease_tokens(member_id, 1)
        await DM(member_id, f'Started a session for you. You have {tokens[0][0]} tokens left.')
    # print(f'Started for {member}')
    else:
        await DM(member_id, f'Not enough tokens to start. Charge up again with !charge')
        # print(f'Not enough tokens for {member}')
    #TODO add to database


if __name__ == '__main__':
    client.run(secrets.discord_token)


