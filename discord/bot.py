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

intents=discord.Intents.all()


client = commands.Bot(command_prefix='!', intents=intents)

db.db_action("CREATE TABLE IF NOT EXISTS users(username text, email text)")
print(db.db_action("SELECT count(*) FROM users"))

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

    tokens = db.get_tokens(member_id)

    DM(member_id, f"Thank you for signing up! You have {tokens} tokens")

    if message.content.startswith('!start'):
        await message.channel.send(f'Started for {member}')
        print(f'Started for {member}')


async def DM(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await client.send_message(user, message)


if __name__ == '__main__':
    client.run(secrets.discord_token)


