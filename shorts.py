from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.editor import AudioFileClip
import random
import whisper
from TikTokTTS.main import tts
import sys
from moviepy.editor import ImageClip
from moviepy.audio.AudioClip import concatenate_audioclips


def transcribe_audio(audio_path,txt):
    model = whisper.load_model("base")
    #transcribe the audio and get the word timestamps
    result = model.transcribe(audio=audio_path,word_timestamps=True)
    segments = result['segments']
    subs = []
    split_text = txt.split(' ')
    i = 0
    for segment in segments:
        for words in segment["words"]:
            subs.append(((words["start"], words["end"]), split_text[i]))
            i+=1
    
    return subs
    
def get_text(file_path):
    with open(file_path, 'r',encoding = "UTF-8") as file:
        return file.read()

def crop_and_center_clip(clip):
    crop_width = (clip.h * (9 / 16))
    crop_height = (crop_width * (16 / 9)) - 200 #200 is offset value 
    clip_cropped = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=int(crop_width), height=int(crop_height))
    return clip_cropped.resize(height=1280)

def cut_video(video_path, video_length):
        #get the video clip
        clip = VideoFileClip(video_path)
        #get a random point in the video. subtract the clip length to make sure the clip is not out of bounds
        random_point = random.randint(0,int(clip.duration-video_length))
        #cut the video where the random poiont starts and add clip length to it
        clip = clip.subclip(random_point, random_point+video_length)
        return crop_and_center_clip(clip)
    
def get_image(image_path,video_width,start,duration, pos=("center","top")):
    img = ImageClip(image_path).set_start(start).set_duration(duration).set_pos(pos).margin(top=300,opacity=0.0)
    img = img.resize(width=int(video_width*0.9))
    return img



def combine_and_write(clip, subtitles, audioclip, output_path,images):
    final = CompositeVideoClip([clip, subtitles]+images)
    final = final.set_audio(audioclip)
    
    final.write_videofile(output_path)

    final.close()

def create_subtitle(subs):
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))

def split_text(text,chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    if(len(sys.argv) < 2):
        print("Session_id for the API is required as an argument. Please provide it as an argument.")
        return
    SESSION_ID = sys.argv[1]
    TEXT = get_text(r'Texts/text.txt')
    VOICE = "en_us_006"
    FINAL_AUDIO_FILE_PATH = r"Audio/voice.mp3"
    img_paths = ["Images/post.png","Images/comment1.png","Images/comment2.png"]
    
    audio_files=[]
    for i,txt in enumerate(split_text(TEXT)):
        AUDIO_FILE_PATH = f"Audio/voice{i}.mp3"
        tts(SESSION_ID, VOICE, txt, AUDIO_FILE_PATH)
        audio_files.append(AudioFileClip(AUDIO_FILE_PATH))
        
    audioclip = concatenate_audioclips(audio_files)
    
    clip = cut_video(r'Videos/min.mp4',audioclip.duration)
    time = 0
    images=[]
    for img in img_paths:
        images.append(get_image(img,clip.w,time,time+2))
        time += 2
    
    subtitles = create_subtitle(transcribe_audio(AUDIO_FILE_PATH,TEXT))
    combine_and_write(clip, subtitles, audioclip, r"Videos/short.mp4",images)

if __name__ == "__main__": main()
