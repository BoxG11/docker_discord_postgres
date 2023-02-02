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

from celery import Celery

print('Application started')
logging.basicConfig(level=logging.INFO)
logging.info('Application started')

app = Celery(
    'postman',
    broker='pyamqp://myuser:mypassword@rabbitmq',
    backend='rpc://myuser:mypassword@rabbitmq',
)


intents = discord.Intents.all()


client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_message(message):
    member = message.author
    member_id = str(message.author.id)

    if message.author == client.user or member_id in db.get_blocked_users():
        return

    db.insert_user(member_id)
    db.insert_message(member_id, message.content)

    if message.content.startswith('!power'):
        try:
            if int(message.content.split(' ')[1]) > 0:
                pass
        
        except:
            await DM(member, f"Please enter a valid power level like: !power 3")
            return

        
        power_lvl = message.content.lower().split(' ')[1]
        print(type(power_lvl))
        print(f"user: {member_id} changed to power level: {power_lvl}")
        tokens_per_hr = db.get_tokens_per_hr(power_lvl)
        #db.power up for user
        await DM(member, f"You are now at power level {power_lvl}. It costs {tokens_per_hr} tokens per hour")
        

    if message.content.startswith('!help'):
        await DM(member, f"sorry, no help for you. go to support or check instructions")

    if message.content.startswith('!start'):
        app.send_task('addTask', (member_id, "start"))
        await DM(member, "Starting session, please wait for confirmation")

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

    if message.content.startswith('!queue'):
        await DM(member, f"Your queue: {str(db.get_tasks())}")


async def DM(member: discord.Member, message):
    channel = await member.create_dm()
    await channel.send(message)


if __name__ == '__main__':
    client.run(secrets.discord_token)


