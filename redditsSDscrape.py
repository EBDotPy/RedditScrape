import discord
from discord.ext import commands
import schedule
import time
import praw
import datetime
from cred import client_id, client_secret, username, password, user_agent, token
# from credentials import client_id, client_secret, username, password, user_agent, token

# create a new bot instance
bot = commands.Bot(command_prefix='!')

def get_top_posts(subreddit, limit=1000):
    # create a new reddit instance
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         username=username, password=password, user_agent=user_agent)
    now = datetime.datetime.now()
    # return the top posts from subreddit
    return [post for post in reddit.subreddit(subreddit).new(limit=limit) if post.link_flair_text == "Workflow Included" and post.created_utc > (now - datetime.timedelta(days=1)).timestamp()]

# define the top_posts command
@bot.command()
async def top_posts(ctx):
    try:
        # get top posts
        posts = get_top_posts('StableDiffusion')[:5]
        # create the output string
        output = '\n'.join([f'{i + 1}: {post.title}\n{post.url}' for i, post in enumerate(posts)])
        # send the output to the channel
        await ctx.send(output)
    except Exception as e:
        # send an error message if something goes wrong
        await ctx.send("An error occured. Please make sure that the subreddit exist or try again later.")

# schedule the top_posts command to run every day at 8am
def job():
    bot.loop.create_task(bot.get_command('top_posts').callback(None, None))
schedule.every().day.at("08:00").do(job)

# run the bot
bot.run(token)

# run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
