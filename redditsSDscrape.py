# Simple program to get some posts and URL form the SD reddit.

import discord
from discord.ext import commands
import schedule
import time
import praw
import datetime
from cred import client_id, client_secret, username, password, user_agent, token
# from credentials import client_id, client_secret, username, password, user_agent, token

bot = commands.Bot(command_prefix='!')

@bot.command()
async def top_posts(ctx):
    try:
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                             username=username, password=password, user_agent=user_agent)
        posts = reddit.subreddit('StableDiffusion').new(limit=1000)
        now = datetime.datetime.now()
        count = 1
        output = ""
        for post in posts:
            if post.link_flair_text == "Workflow Included" and post.created_utc > (now - datetime.timedelta(days=1)).timestamp():
                output += str(count) + ": " + post.title + "\n"
                output += post.url + "\n"
                count += 1
                if count > 5:
                    break
        await ctx.send(output)
    except Exception as e:
        await ctx.send("An error occured. Please make sure that the subreddit exist or try again later.")

def job():
    bot.loop.create_task(bot.get_command('top_posts').callback(None, None))

schedule.every().day.at("08:00").do(job)

bot.run(token)

while True:
    schedule.run_pending()
    time.sleep(1)

