# Purpose 
This project is intended to automize the video editing aspect of creating TikTok/YouTube shorts where there is a reddit post and a text to speech AI narrating it with subtitle and an image displayed paired with gameplay in the background

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
## Technical requirements

* [Visual Studio Code (VSCode)](https://code.visualstudio.com/download) as the IDE
  * [Pythonn]([vscode:extension/Dart-Code.dart-code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)) plugin for VSCode

* [Python](https://docs.flutter.dev/get-started/install](https://www.python.org/downloads/)https://www.python.org/downloads/) 

* [ffmpeg](https://ffmpeg.org/) [Windows installation](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

* [ImageMagick](https://imagemagick.org/script/download.php)
* Install all the python modules in the requiremtn
