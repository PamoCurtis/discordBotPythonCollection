import os
from dotenv import load_dotenv
import requests
from hashlib import new

import discord
from discord.ext import commands





load_dotenv("BOT_TOKENS.env")

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print("Bot is ready to hash some files.")


description = f"""
Upload a file to discord and add following as a comment:

Syntax: (.h | .hash) [algorithm]

Supported hash algorithms:
MD4, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
SHA3_224, SHA3_256, SHA3_384, SHA3_512,
SHAKE_128, SHAKE_256, BLAKE2B, BLAKE2S

default algorithm: MD5
"""
#hashes the binary data of uploaded files by using the python hashlib library
#TODO   shake_128 and shake_256 need some parameters
@bot.command(aliases=['h'],description=description)
async def hash(ctx, hash = 'md5'):

    #checks if file was uploaded
    try:
        attach_url = ctx.message.attachments[0].url
        filename   = ctx.message.attachments[0].filename

        file_req = requests.get(attach_url)
    except:
        await ctx.send("file is missing")
    
    
    try:
        #hashes the binary data of the given file
        hash_msg = new(name = hash, data = file_req.content)
    except:
        await ctx.send(f'{hash} isn\'t supported')

    em = discord.Embed(title = filename)
    em.add_field(name = f'{hash_msg.name} hash:', value = hash_msg.hexdigest())
    
    await ctx.send(embed = em)


bot.run(os.getenv('YOUR_BOT_TOKEN'))
