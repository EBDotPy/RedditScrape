# Simple program to get some posts and URL form the SD reddit.

import discord
from discord.ext import commands
from cred import client_id, client_secret, username, password, user_agent, token
# from credentials import client_id, client_secret, username, password, user_agent, token
import praw
import datetime

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
now = datetime.datetime.now()

@bot.command()
async def top_posts(ctx):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username=username, password=password, user_agent=user_agent)
    posts = reddit.subreddit('StableDiffusion').new(limit=1000)
    count = 1
    output = ""
    for post in posts:
        if post.link_flair_text == "Workflow Included" and post.created_utc > (now - datetime.timedelta(days=1)).timestamp():
            output += str(count) + ": " + post.title + "\n"
            output += "https://www.reddit.com" + post.permalink + "\n"
            count += 1
            if count > 5:
                break
    await ctx.send(output)

bot.run(token)