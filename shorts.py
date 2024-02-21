from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.editor import AudioFileClip
import random
import whisper
from TikTokTTS.main import tts
import sys


def cut_video(video_path, video_length):
        #get the video clip
        clip = VideoFileClip(video_path)
        #get a random point in the video. subtract the clip length to make sure the clip is not out of bounds
        random_point = random.randint(0,int(clip.duration-video_length))
        #cut the video where the random poiont starts and add clip length to it
        clip = clip.subclip(random_point, random_point+video_length)
        return clip

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    #transcribe the audio and get the word timestamps
    result = model.transcribe(audio=audio_path,word_timestamps=True)
    segments = result['segments']
    subs = []
    for segment in segments:
        for words in segment["words"]:
            subs.append(((words["start"], words["end"]), words["word"]))
    
    return subs
    
def get_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def combine_and_write(clip, subtitles, audioclip, output_path):
    final = CompositeVideoClip([clip, subtitles])
    final = final.set_audio(audioclip)
    final.write_videofile(output_path)
    final.close()

def create_subtitle(subs):
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))

    
def main():
    if(len(sys.argv) < 2):
        print("Session_id for the API is required as an argument. Please provide it as an argument.")
        return
    SESSION_ID = sys.argv[1]
    TEXT = get_text(r'Texts/text.txt')
    VOICE = "en_us_006"
    AUDIO_FILE_PATH = r"Audio/voice.mp3"
    
    tts(SESSION_ID, VOICE, TEXT, AUDIO_FILE_PATH)
    audioclip = AudioFileClip(AUDIO_FILE_PATH)
    subtitles = create_subtitle(transcribe_audio(AUDIO_FILE_PATH))
    clip = cut_video('Videos/min.mp4',audioclip.duration)
    combine_and_write(clip, subtitles, audioclip, "Videos/short.mp4")

if __name__ == "__main__": main()

