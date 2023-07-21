from scrape import *
from render import *
from constants import *
import moviepy
from bark import generate_audio
from youtube import *

gen = 0
voice_prompt = "smthn.npz"  # TODO: make a .npz history prompt for a voice
while True:
    gen = gen + 1
    post_ID = getRandomTopPost("askreddit")

    title, posting_user = getTitle(post_ID)
    title_speech = generate_audio(text=title, outputName="title", history_prompt=voice_prompt)
    render(title, posting_user, title_speech, "title")

    comments = getComments(post_ID, NUM_COMMENTS)
    for i, comment in enumerate(comments):
        print(f"Comment {i+1}: {comment['comment']}\nUpvotes: {comment['upvotes']}\nAuthor: {comment['author']}\n")
        comment_speech = generate_audio(text=f"{comment['comment']}", outputName=f"comment{i}", history_prompt=voice_prompt)
        render(comment['comment'], comment['author'], comment_speech, f"comment{i}")

    # concatenate all videos
    video_files = ['title.mp4']
    for i in range(len(comments)):
        video_files.append(f'comment{i}.mp4')

    video_clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(f"final{str(gen)}.mp4")
    upload(title, "New reddit videos EVERYDAY!", "final.mp4","redditVideo_testing/redditBlues.json")