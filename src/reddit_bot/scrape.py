from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def get_post(driver) ->None:
    #shreddit post is the tag name for the post author
    post = driver.find_element(By.TAG_NAME,"shreddit-post")
    assert post is not None, "No post found"
    
    paragraphs = post.find_elements(By.TAG_NAME,"p")
    content = ""
    for p in paragraphs:
        content += p.text + " "
    
    content = content.strip()  # Remove trailing whitespace
    content += " | "  # Add the separator at the end
    
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
      content += p.text
      content += " "
      
    with open(r"Assets/Texts/text.txt", "a",encoding="UTF-8") as file:
      comments_written += 1
      print(f"i: {i} comments_written: {comments_written}")
      if content[-1] != '.': content += "."
      if comments_written != comments_to_get: content += " | "
      file.write(content)
    i += 1
    


def main():
  driver = webdriver.Chrome()
  driver.get("https://www.reddit.com/r/AskReddit/comments/1benjft/what_lifehack_seems_to_be_fake_but_its_a_true/")
  driver.maximize_window()
  get_post(driver)
  get_comments(driver,2)

  
if __name__=="__main__" : main()