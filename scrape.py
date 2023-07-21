import praw
import json
from constants import clientFile, COMMENT_POOL_MODIF, MAX_LENGTH

def getComments(PAGE, NUM_COMMENTS):
    with open(clientFile, "r") as json_file:
        client_secret = json.load(json_file)
        file_client_id = client_secret["client_id"]
        file_client_secret = client_secret["client_secret"]
        file_user_agent = client_secret["user_agent"]

    reddit = praw.Reddit(
        client_id=file_client_id,
        client_secret=file_client_secret,
        user_agent=file_user_agent
    )
    
    submission = reddit.submission(PAGE)

    comments = submission.comments
    comments.replace_more(limit=0)
    top_comments = sorted(comments[:NUM_COMMENTS * COMMENT_POOL_MODIF], key=lambda x: x.score, reverse=True)[:NUM_COMMENTS]

    comment_list = []
    for i, comment in enumerate(top_comments):
        body = str(comment.body.count)
        if len(comment.body) <= MAX_LENGTH:
            comment_list.append({'comment': comment.body, 'upvotes': comment.score, 'author': str(comment.author)})
            if len(comment_list) == 0:
                getComments(PAGE, NUM_COMMENTS)
    return comment_list

def getTitle(PAGE):
    with open(clientFile, "r") as json_file:
        client_secret = json.load(json_file)
        file_client_id = client_secret["client_id"]
        file_client_secret = client_secret["client_secret"]
        file_user_agent = client_secret["user_agent"]

    reddit = praw.Reddit(
        client_id=file_client_id,
        client_secret=file_client_secret,
        user_agent=file_user_agent
    )

    submission = reddit.submission(PAGE)
    return (submission.title, str(submission.author))

def getRandomTopPost(subreddit):
    with open(clientFile, "r") as json_file:
        client_secret = json.load(json_file)
        file_client_id = client_secret["client_id"]
        file_client_secret = client_secret["client_secret"]
        file_user_agent = client_secret["user_agent"]

    reddit = praw.Reddit(
        client_id=file_client_id,
        client_secret=file_client_secret,
        user_agent=file_user_agent
    )

    submission = reddit.subreddit(subreddit).random()
    return submission.id