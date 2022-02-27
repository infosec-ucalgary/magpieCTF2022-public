import discord
import os
from re import search

client = discord.Client()

easyOSINT = "Butchart Garden"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if easyOSINT.lower() in message.content.lower():
        await message.channel.send('magpie{wh3R3_d1D_7h3y_c0M3_Fr0m_wh3r3_D1d_7hEy_60}')


client.run('<key>')