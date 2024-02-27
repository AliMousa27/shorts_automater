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
from typing import List,Tuple
import os
from os import walk

END_OF_IMAGE_MARKER = "|"

    
def get_text(file_path):
    """
    Reads the contents of a file and returns it as a string.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file as a string.
    """
    with open(file_path, 'r',encoding = "UTF-8") as file:
        bad_chars = [';', ':', '!', "*","\n","-"]
    
        return ''.join((filter(lambda i: i not in bad_chars, 
                                    file.read())))




def split_text(text:str, chunk_size=200) -> List[str]:
    """
    Splits the given text into chunks of a specified size.

    Args:
        text (str): The text to be split.
        chunk_size (int, optional): The maximum size of each chunk. Defaults to 200.

    Returns:
        list: A list of chunks, where each chunk is a string.

    Example:
        >>> text = "Lore ipsum dolor sit amet, consectetur adipiscing elit."
        >>> split_text(text, chunk_size=10)
        ['Lore ipsum', 'dolor sit', 'amet,', 'consectetur', 'adipiscing', 'elit.']
    """
    words : List[str] = text.split(' ')
    chunks : List[str] = []
    chunk = ''
    for word in words:
        if len(chunk) + len(word) <= chunk_size:
            chunk += ' ' + word
        else:
            chunks.append(chunk)
            chunk = word
    chunks.append(chunk)
    return chunks

def crop_and_center_clip(clip: VideoFileClip)-> VideoFileClip:
    """
    Crop and center the given video clip to fit a 9:16 aspect ratio.

    Parameters:
    clip (VideoFileClip): The video clip to be cropped and centered.

    Returns:
    VideoFileClip: The cropped and centered video clip.
    """
    crop_width = (clip.h * (9 / 16))
    crop_height = (crop_width * (16 / 9)) - 200 #200 is offset value 
    clip_cropped = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=int(crop_width), height=int(crop_height))
    return clip_cropped.resize(height=1280)

def cut_video(video_path:str, video_length: int) -> VideoFileClip:
    """
    Cuts a video clip from the given video_path starting from a random point and with the specified length.

    Parameters:
    video_path (str): The path of the video file.
    video_length (int): The desired length of the video clip in seconds.

    Returns:
    VideoFileClip: The cropped and centered video clip.
    """
    clip = VideoFileClip(video_path)
    random_point = random.randint(0,int(clip.duration-video_length))
    clip = clip.subclip(random_point, random_point+video_length)
    return crop_and_center_clip(clip)

def get_image(image_path:str,video_width:int,start:int,duration:int, pos=("center","top")) -> ImageClip:
    """

    Parameters:
    image_path (str): The path to the image file.
    video_width (int): The width of the video.
    start (int): The start time where the image gets show in seconds
    duration (int): The duration of how long the iamge will be shown relative to the start parameter
    pos (tuple, optional): The position of the clip on the screen. Defaults to ("center","top").

    Returns:
    ImageClip: The ImageClip object with the specified properties.
    """
    img = ImageClip(image_path).set_start(start).set_duration(duration).set_pos(pos).margin(top=300,opacity=0.0)
    img = img.resize(width=int(video_width*0.9))
    return img

def create_subtitle(subs: str) -> SubtitlesClip:
    """
    Create a subtitle clip using the given text.

    Args:
        subs (str): The text for the subtitle.

    Returns:
        SubtitlesClip: The generated subtitle clip.
    """
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=100, color='white')
    return SubtitlesClip(subs, generator).set_position(('center'))



def transcribe_audio(audio_file_path: str, txt: str):
    """
    Transcribes the audio file and extracts word timestamps and image durations.

    Args:
        audio_file_path (str): The path to the audio file.
        txt (str): The text to be transcribed.

    Returns:
        Tuple[List[Tuple[int, int], str], List[Tuple[int, int]]]: A tuple containing two lists.
            The first list contains tuples of word timestamps in the format (start, end, word).
            The second list contains tuples of image durations in the format (start, end).
    """
    model = whisper.load_model("base")  
    subs: List[Tuple[int, int], str] = []
    split_text = txt.split()
    i = 0
    total_time = 0.0
    image_durations: List[Tuple[int, int]] = []
    image_start = 0

    result = model.transcribe(audio=audio_file_path, word_timestamps=True)
    segments = result['segments']
    duration = AudioFileClip(audio_file_path).duration
    for segment in segments:
        for words in segment["words"]:
            if i < len(split_text) and split_text[i] == END_OF_IMAGE_MARKER:
                image_durations.append((image_start, words["end"] + total_time))
                image_start = words["end"] + total_time
                subs.append(((words["start"] + total_time, words["end"] + total_time), words["word"]))
            i += 1
            subs.append(((words["start"] + total_time, words["end"] + total_time), words["word"]))
    total_time += duration
    image_durations.append((image_durations[-1][1], total_time))
    return (subs, image_durations)

def combine_and_write(clip:VideoFileClip, subtitles:SubtitlesClip, audioclip:AudioFileClip, output_path:str, images:List[ImageClip]):
    """
    Combines the given video clip, subtitles, images, and audio clip into a final composite video clip.
    The final composite clip is then written to the specified output path.

    Args:
        clip (VideoClip): The main video clip.
        subtitles (list): List of subtitle clips to be added to the main video clip.
        audioclip (AudioClip): The audio clip to be added to the final composite video clip.
        output_path (str): The path where the final composite video clip will be saved.
        images (list): List of image clips to be added to the final composite video clip.

    Returns:
        None
    """
    #concatante the lists of images and subtitles and the video
    final = CompositeVideoClip([clip, subtitles] + images)
    final = final.set_audio(audioclip)
    final = final.set_duration(audioclip.duration)
    # Ensure the final duration is the same as the audio duration as the image clips durations get added to the composite clip and produce an empty clip 
    #NOTE: speicfy the threads based on the specs of your system 
    final.write_videofile(output_path, threads=8)
    final.close()
    
def get_file_paths(directory: str):
    """
    Returns a list of file paths in the specified directory.

    Args:
        directory (str): The directory path.

    Returns:
        list: A list of file paths.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def main():
    if(len(sys.argv) < 2):
        print("Session_id for the API is required as an argument. Please provide it as an argument.")
        return
    SESSION_ID = sys.argv[1]
    TEXT = get_text(r'Texts/text.txt')
    VOICE = "en_us_006"
    files=get_file_paths("Images")
    print(files)        
    
    img_paths = ["Images/post.png","Images/comment1.png","Images/comment2.png"]

    audio_files : List[AudioFileClip] = []
    audio_files_paths: List[str] = []
    for i,txt in enumerate(split_text(TEXT)):
        AUDIO_FILE_PATH = f"Audio/voice{i}.mp3"
        audio_files_paths.append(AUDIO_FILE_PATH)
        tts(SESSION_ID, VOICE, txt, AUDIO_FILE_PATH)
        audio_files.append(AudioFileClip(AUDIO_FILE_PATH))
        
    FINAL_AUDIO_PATH = r"Audio/concatenated_audio.mp3"
    audioclip : AudioFileClip = concatenate_audioclips(audio_files)
    
    audioclip.write_audiofile(FINAL_AUDIO_PATH)
    #the subtitles currently is a list of tuples of the start and end time of each word and the word itself
    subtitles, image_durations = transcribe_audio(FINAL_AUDIO_PATH, TEXT)
    #now the subtitles are a list of subtitle clips
    subtitles = create_subtitle(subtitles)    

    clip : VideoFileClip = cut_video(r'Videos/min.mp4',audioclip.duration)
    
    time = 0
    images : List[ImageClip] = []
    for img, time in zip(img_paths, image_durations):
        images.append(get_image(img,clip.w,time[0],time[1]))

    combine_and_write(clip, subtitles, audioclip, r"Videos/short.mp4",images)

if __name__ == "__main__": main()