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

def get_top_posts(subreddit, limit=1000):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         username=username, password=password, user_agent=user_agent)
    now = datetime.datetime.now()
    return [post for post in reddit.subreddit(subreddit).new(limit=limit) if post.link_flair_text == "Workflow Included" and post.created_utc > (now - datetime.timedelta(days=1)).timestamp()]

@bot.command()
async def top_posts(ctx):
    try:
        posts = get_top_posts('StableDiffusion')[:5]
        output = '\n'.join([f'{i + 1}: {post.title}\n{post.url}' for i, post in enumerate(posts)])
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

