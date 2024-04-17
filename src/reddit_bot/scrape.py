from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from typing import List
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
def validate_post(url:str):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  soup = soup.find("shreddit-post")

  if soup.find(name="shreddit-embed") or soup.find(name="shreddit-player") or soup.find(name="img"):
    print("Found video or image in the post. Tool is menat ot be used only for text based posts")
    exit(1)

    
def get_post(driver: WebDriver) ->None:
    #shreddit post is the tag name for the post author
    validate_post(driver.current_url)
    try:
        post: WebElement = WebDriverWait(driver,timeout=20).until(EC.presence_of_element_located((By.TAG_NAME,"shreddit-post")))
    except NoSuchElementException as e:
      print(f"there is no post: {e}")
      exit(1)


    content: str = post.get_attribute("post-title")  
    paragraphs: List = post.find_elements(By.TAG_NAME,"p")
    content +=" ".join([p.text for p in paragraphs])
    
    content += " | " 
    print(f"content of the post is {content}")
    
    
    post.screenshot(r"Assets/images/+.png")#called it + because its the first and its gonna be before the commetns taht arre 0....comments
    #write the content to the text file
    with open(r"Assets/Texts/text.txt", "a") as file:
        content = bytes(content, 'utf-8').decode('utf-8', 'ignore')
        file.write(content)
    
def get_comments(driver: WebDriver, comments_to_get: int):
  #https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
  driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
  
  #TODO make it wait instead of sleep
  #sleep(5)
  
  comments_written = 0
  i = 1
  
  try:
  #comments = driver.find_elements(By.TAG_NAME,"shreddit-comment")
    comments = WebDriverWait(driver,timeout=20).until(EC.presence_of_all_elements_located((By.TAG_NAME,"shreddit-comment")))
  except TimeoutException as e:
    print("Page took too long to wait")
    exit(1)
  while comments_written < comments_to_get and i < len(comments):
    if comments[i].get_attribute("depth") != "0":
      i += 1
      continue
    #https://stackoverflow.com/questions/8922107/javascript-scrollintoview-middle-alignment
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comments[i])
    comments[i].screenshot(f"Assets/images/{i}.png")
    content = ""
    for p in comments[i].find_elements(By.TAG_NAME,"p"):
      print(f"CURRENT COMMENT: {p.text}")
      content += p.text
      if content[-1] != '.':
        content+='.'
      content += " "
      
    with open(r"Assets/Texts/text.txt", "a",encoding="UTF-8") as file:
      comments_written += 1
      print(f"i: {i} comments_written: {comments_written}")
      if comments_written != comments_to_get: content += " | "
      #turn the string to bytes, then back to a string but ignore chars that cause an error when they arent supported by the encoding format
      content = bytes(content, 'utf-8').decode('utf-8', 'ignore')
      file.write(content)
    i += 1
    


def scrape(url: str):
  assert url is not None, "No url provided"
  assert url.startswith("https://www.reddit.com/r/"), "The url needs to be reddit"
  driver = webdriver.Chrome()
  driver.get(url)
  driver.maximize_window()
  try:
    get_post(driver)
    get_comments(driver,2)
  except Exception as e:
    print(f"Error scraping the post: {e}")
    exit(1)
  
