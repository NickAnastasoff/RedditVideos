#!/usr/bin/env python3
import sys
from scrape import *
from render import *
from Constants import *
import moviepy
from audioProccessing import textToBark # type: ignore
from GptProccessing import * # type: ignore
from Youtube import * # type: ignore

gen = 0

while True:
    gen = gen + 1
    post_ID = getRandomTopPost("askreddit")

    title, posting_user = getTitle(post_ID)
    title_speech = textToBark(text=title, outputName="title", history_prompt='joeRogan.npz')
    render(title, posting_user, title_speech, "title")

    comments = getComments(post_ID, NUM_COMMENTS)
    for i, comment in enumerate(comments):
        print(f"Comment {i+1}: {comment['comment']}\nUpvotes: {comment['upvotes']}\nAuthor: {comment['author']}\n")
        #commetary = promptGPT(False, f"be critical of the following text in a joking manor: {comment['comment']} \ill try! The")
        comment_speech = textToBark(text=f"{comment['comment']}", outputName=f"comment{i}", history_prompt='joeRogan.npz') #The {commetary}", f"comment{i}")
        render(comment['comment'], comment['author'], comment_speech, f"comment{i}")

    # concatenate all videos
    video_files = ['title.mp4']
    for i in range(len(comments)):
        video_files.append(f'comment{i}.mp4')

    video_clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(f"final{str(gen)}.mp4")
    #upload(title, "New reddit videos EVERYDAY!\n\nPlease leave comments on what should change!", "final.mp4","redditVideo_testing/redditBlues.json")