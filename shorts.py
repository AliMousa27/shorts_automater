

from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip, CompositeVideoClip
import random
subs = [((0, 1), "This"),
        ((1,2), "is"),
        ((2,3), "a"),
        ((3,4), "test"),
        ((4,5), "of"),
        ((5,6), "the"),
        ((7,8), "subtitles",)]


def cut_video(video_path, clip_length=10):
        clip = VideoFileClip(video_path)
        random_point = random.randint(0,int(clip.duration-clip_length))
        clip = clip.subclip(random_point, random_point+clip_length)
        return clip
    
    
def create_subtitle(subs):
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))

clip = cut_video('min.mp4')
subtitles = create_subtitle(subs)
final = CompositeVideoClip([clip, subtitles])
final.write_videofile("short.mp4")
final.close()

