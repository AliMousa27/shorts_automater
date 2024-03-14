from selenium import webdriver
from selenium.webdriver.common.by import By



def get_post(driver) ->None:
    #shreddit post is the tag name for the post author
    post = driver.find_element(By.TAG_NAME,"shreddit-post")
    content =post.find_element(By.TAG_NAME,"h1").text
    content += " | "
    post.screenshot(r"Assets/images/0.png")
    #write the content to the text file
    with open(r"Assets/Texts/text.txt", "a") as file:
      file.write(content)
    



def main():
  driver = webdriver.Chrome()
  driver.get("https://www.reddit.com/r/AskReddit/comments/1benikn/what_invention_was_so_good_that_it_actually_cant/")
  get_post(driver)
  
  while True:
    pass
  
if __name__=="__main__" : main()