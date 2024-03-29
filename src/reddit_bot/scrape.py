from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
def get_post(driver: WebDriver) ->None:
    #shreddit post is the tag name for the post author
    try:
        post: WebElement = driver.find_element(By.TAG_NAME,"shreddit-post")
    except NoSuchElementException as e:
      print(f"there is no post: {e}")
      #TODO: then that means that we have a bunch of paragraphs to get so add code to get them
      pass
    content: str = post.get_attribute("post-title")  
    content += " | " 
    
    post.screenshot(r"Assets/images/+.png")#called it + because its the first and its gonna be before the commetns taht arre 0....comments
    #write the content to the text file
    with open(r"Assets/Texts/text.txt", "a") as file:
        file.write(content)
    
def get_comments(driver, comments_to_get: int):
  #https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
  driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
  #TODO make it wait instead of sleep
  sleep(5)
  
  comments_written = 0
  i = 1
  comments = driver.find_elements(By.TAG_NAME,"shreddit-comment")
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
  
