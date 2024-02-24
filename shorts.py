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

END_OF_IMAGE_MARKER = "|"

def get_text(file_path):
    with open(file_path, 'r',encoding = "UTF-8") as file:
        return file.read()

def split_text(text,chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def crop_and_center_clip(clip):
    crop_width = (clip.h * (9 / 16))
    crop_height = (crop_width * (16 / 9)) - 200 #200 is offset value 
    clip_cropped = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=int(crop_width), height=int(crop_height))
    return clip_cropped.resize(height=1280)

def cut_video(video_path, video_length):
    clip = VideoFileClip(video_path)
    random_point = random.randint(0,int(clip.duration-video_length))
    clip = clip.subclip(random_point, random_point+video_length)
    return crop_and_center_clip(clip)

def get_image(image_path,video_width,start,duration, pos=("center","top")):
    img = ImageClip(image_path).set_start(start).set_duration(duration).set_pos(pos).margin(top=300,opacity=0.0)
    img = img.resize(width=int(video_width*0.9))
    return img

def create_subtitle(subs):
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))

def transcribe_audio(audio_paths, txt):
    model = whisper.load_model("base")
    subs = []
    split_text = txt.split()
    i = 0
    total_time = 0.0
    image_durations = []
    image_start=0
    for audio_path in audio_paths:
        result = model.transcribe(audio=audio_path, word_timestamps=True)
        segments = result['segments']
        duration = AudioFileClip(audio_path).duration
        for segment in segments:
            for words in segment["words"]:
                if i < len(split_text ):
                    if split_text[i] == END_OF_IMAGE_MARKER:
                        i += 1
                        image_durations.append((image_start,words["end"]+total_time))
                    subs.append(((words["start"] + total_time, words["end"] + total_time), split_text[i]))
                    i += 1
                else:
                    subs.append(((words["start"] + total_time, words["end"] + total_time), words["word"]))
        total_time += duration
    #add the last image duration
    image_durations.append((image_durations[-1][1],total_time))
    return (subs, image_durations)

def combine_and_write(clip, subtitles, audioclip, output_path,images):
    final = CompositeVideoClip([clip, subtitles]+images)
    final = final.set_audio(audioclip)
    final.write_videofile(output_path)
    final.close()

def main():
    if(len(sys.argv) < 2):
        print("Session_id for the API is required as an argument. Please provide it as an argument.")
        return
    SESSION_ID = sys.argv[1]
    TEXT = get_text(r'Texts/text.txt')
    VOICE = "en_us_006"
    img_paths = ["Images/post.png","Images/comment1.png","Images/comment2.png"]

    audio_files=[]
    audio_files_paths=[]
    for i,txt in enumerate(split_text(TEXT)):
        AUDIO_FILE_PATH = f"Audio/voice{i}.mp3"
        audio_files_paths.append(AUDIO_FILE_PATH)
        tts(SESSION_ID, VOICE, txt, AUDIO_FILE_PATH)
        audio_files.append(AudioFileClip(AUDIO_FILE_PATH))
        
    audioclip = concatenate_audioclips(audio_files)
    subtitles, image_durations = transcribe_audio(audio_files_paths, TEXT)
    subtitles = create_subtitle(subtitles)    
    clip = cut_video(r'Videos/min.mp4',audioclip.duration)
    
    time = 0
    images=[]
    for img, time in zip(img_paths, image_durations):
        images.append(get_image(img,clip.w,time[0],time[1]-time[0]))
    combine_and_write(clip, subtitles, audioclip, r"Videos/short.mp4",images)

if __name__ == "__main__": main()