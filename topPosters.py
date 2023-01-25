#simple script to get top 10 posters by subreddit/time

import praw
from collections import Counter
from cred import client_id, client_secret, username, password, user_agent, token

# Create a PRAW instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Get the subreddit name from the user
subreddit_name = input("Enter the subreddit name: ")
nsfw_status = input("Is the subreddit nsfw (yes/no): ")
if nsfw_status.lower() == "yes":
    over18 = True
else:
    over18 = False

# Get the time period from the user
time_period = input("Enter the time period (hour/week/month/year): ")

# Get the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Define a dictionary to store the different time periods and their corresponding PRAW function and parameters
time_periods = {
    "hour": subreddit.new(limit=1000),
    "week": subreddit.top(time_filter='week', limit=1000),
    "month": subreddit.top(time_filter='month', limit=1000),
    "year": subreddit.top(time_filter='year', limit=1000),
    "alltime": subreddit.top(limit=1000)
}

submissions = time_periods.get(time_period, "Invalid time period")

if submissions == "Invalid time period":
    print("Invalid time period")
    exit()

posters = [submission.author.name for submission in submissions if submission.author is not None]
top_posters = Counter(posters)

#Ask the user how many posters they want to see
num_posters = int(input("Enter the number of top posters you want to see: "))

#Print the top num_posters posters
for poster, count in top_posters.most_common(num_posters):
    print(poster)


# Use the subreddit or user option. Which lead to sub options. Use click.
# Time is hour, week, month, year, all time

# Subreddit option: FIRST ask if nsfw or not, then ask for top X posters in Y time as a numbered lists of users,
# or top X posts permalinks in Y time
# User option: X top upvoted comments as a string + permalink in Y time, posts that contain "keyword/phrase"
# in all comments in Y time + permalink