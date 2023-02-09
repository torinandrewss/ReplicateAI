
from instabot import Bot
from secret import password,user
import os 
import glob
from PIL import Image
import random
import contentGen as cg


cookie_del = glob.glob("config/*cookie.json")
if (len(cookie_del)>=1):
    os.remove(cookie_del[0])

caption = cg.generateCaptions()

# Make a 1/3 chance of the image being generated as a variation or from the prompt
rand=random.randint(1,3)
if (rand==1):
    
    image = cg.generateImages1(caption)
else:
    image = cg.generateImages()


im1 = Image.open(image)
im1.save(image[:-4]+".jpg")

image = image[:-4]+".jpg"

print(f"Caption is: {caption}")

try:
    
    bot = Bot()
    bot.login(username=user,password=password)
    

    bot.upload_photo(image,caption=caption)
except:
    print('Error')
finally:
    bot.logout()
    print('logging out')

