from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, urllib.request, requests
import json
from PIL import Image

PATH = "/Users/torinandrews/Desktop/code projects/reLiveAI/src/chromedriver"

driver = webdriver.Chrome(PATH)


# Logging in
def log_in():
    driver.get("https://www.instagram.com/")

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "username")))

    username_loc = driver.find_element(by=By.NAME, value="username")
    username_loc.send_keys(USERNAME)
    pass_loc = driver.find_element(by=By.NAME, value='password')
    pass_loc.send_keys(PASS)
    driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/button').click()

def switch_window():
    time.sleep(8)
    driver.get(f"https://www.instagram.com/{ACCOUNT}")
    
def scroll_and_get_posts():
    '''
    Scrolls down the page and gets all visible posts on that page using get_posts().
    Returns a list of links
    '''
    posts = []
    scrolldown=driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match=False
    while(match==False):
        try:
            posts_visible = get_posts()
            for post in posts_visible:
                if post not in posts:
                    posts.append(post)

            last_count = scrolldown
            time.sleep(4)
            scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            if last_count==scrolldown:
                
                match=True
                
        except selenium.common.exceptions.StaleElementReferenceException:
            
            pass
            
   
    return posts

def get_posts():
    '''
    Returns a list of links as strings. Each link is a post on the profile
    '''
    posts = []
    links = driver.find_elements(by=By.TAG_NAME, value="a")
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)
    return posts

def get_captions_and_alt_from_posts(posts):
    '''
    Takes as input a list of links. Returns two lists of strings(captions, and image alt text)
    '''
    captions = []
    alt_text = []
    src_list=[]
    for link in posts:
        driver.get(link)
        time.sleep(2)
        try:
            caption = driver.find_element(by=By.TAG_NAME, value="h1")
            captions.append(caption.text)

            images = driver.find_elements(by=By.TAG_NAME, value="img")
            for i, img in enumerate(images):
                if img.get_attribute('sizes')!='':
                    # Because selenium cant find 'alt' tag I have to do outerHTML
                    # And then pass to a string strip function
                    text = img.get_attribute('outerHTML')
                    src = img.get_attribute('src')
                    src_list.append(src)
                    element = extract_alt_from_img_tag(text)

                    if element not in alt_text:
                        alt_text.append(element)
        except:
            continue

    return alt_text,captions,src_list
    

def extract_alt_from_img_tag(string):
    '''
    This is a workaround for .get_attribute('alt') not working.
    Cuts the alt section from a string and only returns the value.
    '''
    new_string=""
    i = string.find('alt')
    while string[i] != '"':
        i+=1
    i+=1
    while string[i] != '"':
        new_string+=string[i]
        i+=1
    return new_string

def to_dict(prompts, completions):
    new_dict=  {}
    for i, prompt in enumerate(prompts):
        if (i < len(completions)-1):
            if completions[i] not in new_dict.values():
                new_dict[prompt] = completions[i]
    return new_dict

def export_as_training_data(dict,output_path,append=False):
    '''
    (dict,String,Bool) -> generates JSON file in training data form
    '''
    data = []
    for i, key in enumerate(dict.keys()):
        new_dict = {"prompt":"","completion":""}
        new_dict["prompt"] = key
        new_dict["completion"] = dict[key]
        data.append(new_dict)

    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')

    print('Wrote {} records to {}'.format(len(data), output_path))

def crop_center(pil_img, crop_width, crop_height):
    # Helper Function
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    #Helper Function
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def get_image_and_parse(imgSrcList):
    """
    Gets the image from the page and formats it properly for image variation generation
    """
    for i in range(len(imgSrcList)):
        urllib.request.urlretrieve(imgSrcList[i],"data/images/img{}.png".format(i))
        im = Image.open(f"data/images/img{i}.png")
        new_im = crop_max_square(im)
        new_im.save(f"data/images/img{i}.png",quality=90)





def main():
    
    log_in()
    switch_window()
    posts = scroll_and_get_posts()
    x = get_captions_and_alt_from_posts(posts)
    get_image_and_parse(x[2])
    export_as_training_data(to_dict(x[0],x[1]),"data/data.json")


if ("__name__" == "__main__"):
    USERNAME = input("Your Username: ")
    PASS = input("Your Password: ")
    ACCOUNT = input("Account to copy (username): ")
    main()
    time.sleep(5)
    driver.quit()
