<div align="center">
   <img src="https://media.tenor.com/s1Y9XfdN08EAAAAi/bot.gif" alt="Bot Image">
</div>



# Purpose 
This project aims to streamline the video editing process for creating engaging TikTok/YouTube shorts. It combines Reddit posts, text-to-speech narration, subtitles, and gameplay footage to produce captivating content.

# Scope and Future Features
The current scope is rather limited but I plan to expand this project and flesh it out. Here are some features that I plan on adding
* A bot that scrapes trendy reddit posts from popular subredits, takes a screenshot of the comment and copies the text that is to be turned into subtitles
* A seperate script that takes a gameplay video and a viral video, combines the 2 in a vertical manner and subtitles the clip
* An autonomous system that fully manages the process of scraping and uploading the product videos to a channel on various platforms

# Sample
https://github.com/AliMousa27/shorts_automater/assets/114988369/831d1044-0c1d-4b84-b1ed-89d5a76b8d64

**lol**

# Assets Setup
1. Find a reddit post, copy the post and 1/2 or more comments into the file Assets/Texts/text.txt.
* **IMPORTANT Seperate the comments and post by using the character _|_**
* * Example: This is the text of the post | where this is the comment | and this is some other comment
* Take screenshots of the post and the comments to display them in the video.
* * **IMPORTANT: The images are displayed in alphabetical order. Therefore make sure their order aligns with the order of the text you pasted**
* Download a mp4 file of gameplay of your choice, place it inside of Assets/Videos/ and call the file **min.mp4**
## Technical requirements

* [Visual Studio Code (VSCode)](https://code.visualstudio.com/download) as the IDE
  * [Python plugin for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python) 

* [Python](https://www.python.org/downloads)

* [ffmpeg](https://ffmpeg.org/) [Windows installation](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

* [ImageMagick](https://imagemagick.org/script/download.php)
* Install all the python modules in the [requirements.txt](https://github.com/AliMousa27/shorts_automater/blob/main/src/requirements.txt) file using ```pip install -r requirements.txt```

 * Get a tiktok session ID token. For more information refer to this [readme](https://github.com/AliMousa27/shorts_automater/blob/main/src/TikTokTTS/readme.md)

### Running the program
To run the program, all you have to do is provide the session id in the arguemtns and thats it!
