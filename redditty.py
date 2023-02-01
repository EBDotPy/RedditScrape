import praw
import click
from collections import Counter
from cred import client_id, client_secret, username, password, user_agent, token
from parameters import time_periods

# Create a PRAW instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Define the main function
@click.command()
@click.option("--option", type=click.Choice(["subreddit", "user"]))
def main(option):
    if option == "subreddit":
        subreddit()
    elif option == "user":
        user()

def subreddit():
    # Subreddit option
    nsfw = click.confirm("Is the subreddit NSFW?", default=False)
    subreddit_name = click.prompt("Enter the subreddit name")
    time_period = click.prompt("Enter the time period",
                               type=click.Choice(["hour", "week", "month", "year", "all"]))
    num_posters = click.prompt("Enter the number of top posters you want to display", type=int)
    subreddit = reddit.subreddit(subreddit_name)
    if time_period == "all":
        submissions = subreddit.new(limit=1000)
    else:
        submissions = subreddit.top(time_filter=time_period, limit=1000)

    posters = [submission.author.name for submission in submissions if submission.author is not None]
    top_posters = Counter(posters)
    # Print the top num_posters posters
    for i, (poster, count) in enumerate(top_posters.most_common(num_posters)):
        click.echo(f"{i + 1}. {poster}")


def user():
    # User option
    username = click.prompt("Enter the username")
    user = reddit.redditor(username)
    time_period = click.prompt("Enter the time period",
                               type=click.Choice(["hour", "week", "month", "year", "all"]))
    # Handle time
    comments = user.comments.top(time_filter=time_period, limit=1000)
    if time_period == "all":
        comments = user.comments.new(limit=1000)
    else:
        comments = user.comments.top(time_filter=time_period, limit=1000)
    top_key = click.prompt("Do you want to see top posts, or search for keyphrase?",
                           type=click.Choice(["top", "key"]))
    # Handle top comments (add posts later)
    if top_key == "top":
        top(username, time_period)
    elif top_key == "key":
        key(username, time_period)

def top(username, time_period):
    # Top upvoted X comments in Y period
    num_comments = click.prompt("Enter the number of top upvoted comments you want to see", type=int)
    user = reddit.redditor(username)
    comments = user.comments.top(time_filter=time_periods[time_period], limit=1000)
    for i, comment in enumerate(comments):
        if i == num_comments:
            break
        click.echo(f"{i + 1}. {comment.body} - https://www.reddit.com{comment.permalink}\n")

def key(username, time_period):
    # Keyword that appears in X number of comments over Y time from Z user
    num_comments = click.prompt("Enter the number of comments you want to see", type=int)
    keyword = click.prompt("Enter keyword/phrase").lower()
    user = reddit.redditor(username)
    comments = user.comments.new(limit=1000)
    for i, comment in enumerate(comments):
        if i == num_comments:
            break
        if keyword in comment.body.lower():
            click.echo(f"{i + 1}. {comment.body} - https://www.reddit.com{comment.permalink}\n")

if __name__ == "__main__":
    main()
