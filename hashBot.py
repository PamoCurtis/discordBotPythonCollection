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


#hashes the binary data of uploaded files by using the python hashlib library
#TODO   shake_128 and shake_256 need some parameters
@bot.command(aliases=['h'],description="(.hash | .h) md5|sha1|sha224|sha256|sha384|sha512|sha3_224|sha3_256|sha3_384|sha3_512|shake_128|shake_256|blake2b|blake2s) (file|url)\ndefault is MD5")
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