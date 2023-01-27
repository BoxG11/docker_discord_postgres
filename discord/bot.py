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
    memberid = str(message.author.id)

    if message.author == client.user:
        return
    
    sql = f"INSERT INTO users (username, email) VALUES ('{memberid}', '{message.content}');"
    #await message.channel.send(sql)
    db.db_action(str(sql))

    logging.basicConfig(filename='discord.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug("Message: " + message.content + " | Author: " + str(message.author) + " | Time: " + str(datetime.datetime.now()))

    sql = f"SELECT count(*) FROM users;"
    nr = db.db_action(str(sql))
    await message.channel.send(nr)

    if message.content.startswith('!start'):
        await message.channel.send(f'Started for {member}')
        print(f'Started for {member}')


if __name__ == '__main__':
    client.run(secrets.discord_token)


