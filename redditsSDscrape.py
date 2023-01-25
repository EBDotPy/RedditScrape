# Simple program to get some posts and URL form the SD reddit.

import praw
import datetime
from cred import client_id, client_secret, username, password, user_agent
# from credentials import client_id, client_secret, username, password, user_agent

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     username=username, password=password, user_agent=user_agent)


# Get the current time
now = datetime.datetime.now()

# File name format
file_name = "StableDiffusion_top_posts_{}.txt".format(now.strftime("%Y-%m-%d"))

# Open the file for writing
with open(file_name, "w") as f:
    # Get the top 5 posts from the last 24 hours with the flair "Workflow Included" from the "StableDiffusion" subreddit
    posts = reddit.subreddit('StableDiffusion').new(limit=1000)
    count = 1
    for post in posts:
        if post.link_flair_text == "Workflow Included" and post.created_utc > (now - datetime.timedelta(days=1)).timestamp():
            f.write(str(count) + ": " + post.title + "\n")
            f.write(post.permalink + "\n")
            count += 1
            if count > 5:
                break
