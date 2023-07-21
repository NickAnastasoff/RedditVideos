import random
from moviepy.editor import *
import textwrap
from constants import *

def render(title, posting_user, audio_clip, output_name):
    """
    Renders the title and postingUser on top of the video
    :param title: The title of the video
    :param postingUser: The postingUser of the video
    :param audio_clip: The audio clip to use for the video
    :return: rendered moviepy clip
    """
    videoFile = pathToVideos + random.choice([f for f in os.listdir(pathToVideos) if not f.endswith('.DS_Store')])
    # Get a video from directory
    video_clip = VideoFileClip(videoFile)

    # Set the width of the background ColorClip to be screen width - (LEFT_PADDING + RIGHT_PADDING)
    background_width = video_clip.w - (LEFT_PADDING + RIGHT_PADDING)

    # Wrap the title text to fit within the background width
    wrapped_title = textwrap.fill(title, width=int(background_width / (TITLE_FONT_SIZE * 0.7)))

    # Create a TextClip for the postingUser
    postingUser_clip = TextClip(posting_user, fontsize=POSTING_USER_FONT_SIZE, color='white')

    # Create a TextClip for the title
    title_clip = TextClip(wrapped_title, fontsize=TITLE_FONT_SIZE, color='white', align='West')

    # Create a ColorClip for the background of the box
    background_clip = ColorClip(size=(background_width, title_clip.h + 100), color=(0, 0, 0))

    # Composite the TextClips on top of the background ColorClip
    composite_clip = CompositeVideoClip([background_clip,
                                        postingUser_clip.set_position((LEFT_PADDING, 20)),
                                        title_clip.set_position((LEFT_PADDING, 80))])

    # Set the duration of the composite clip to match the audio clip plus 1 second
    composite_clip = composite_clip.set_duration(audio_clip.duration)

    # Overlay the composite clip on top of the video clip
    final_clip = CompositeVideoClip([video_clip, composite_clip.set_position(('center', 'center'))])

    # Set the audio of the final clip to be the audio clip
    final_clip = final_clip.set_audio(audio_clip).set_duration(audio_clip.duration)

    # Write the final clip to a file
    return final_clip.write_videofile(f"{output_name}.mp4", fps=24)