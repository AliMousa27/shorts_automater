from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.editor import AudioFileClip
import random
import whisper
from TikTokTTS.main import tts

def cut_video(video_path, clip_length=10):
        clip = VideoFileClip(video_path)
        random_point = random.randint(0,int(clip.duration-clip_length))
        clip = clip.subclip(random_point, random_point+clip_length)
        return clip

def transcribe_audio(audio_path):
    #WORDS_INDEX_IN_SEGMENTS_ARRAY = 2
    model = whisper.load_model("base")

    result = model.transcribe(audio=audio_path,word_timestamps=True)
    segments = result['segments']
    subs = []
    for segment in segments:
        for words in segment["words"]:
            subs.append(((words["start"], words["end"]), words["word"]))
    return subs
    
    
    
def create_subtitle(subs):
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))

def main():
    text = "Hello zepei, i just wanna let you know that your super fucking gay man. My hog is throbbing. This is so fucking gay i cant do it anymore i wanna kill myself"
    voice = "en_us_006"
    #TODO make env var
    session_id = "30ca901865d6637c66a138dde47e1334"
    tts(session_id, voice, text, "voice.mp3")
    
    clip = cut_video('min.mp4')
    subtitles = create_subtitle(transcribe_audio("voice.mp3"))
    
    audioclip = AudioFileClip("voice.mp3")

    final = CompositeVideoClip([clip, subtitles])
    final.set_audio(audioclip)
    final.write_videofile("short.mp4")
    final.close()

if __name__ == "__main__": main()