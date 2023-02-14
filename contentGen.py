import os
import openai
import json
import random
import requests
from secret import key,engine


openai.api_key = key

def get_prompts(jsonFile):
    dics = []
    prompts = []
    with open(jsonFile) as f:
       for line in f:
           dics.append(json.loads(line)) 

    for dic in dics:
        prompts.append(dic["prompt"])
    return prompts

prompts = get_prompts("data/personalProfileData.json")

def get_completions(jsonFile):
    dics = []
    completions = []
    with open(jsonFile) as f:
       for line in f:
           dics.append(json.loads(line)) 

    for dic in dics:
        completions.append(dic["completion"])
    return completions

comps = get_completions("data/personalProfileData.json")


def generateCaptions():
    """
    Takes a prompt or a completion from above and generates a caption with the AI.
    Returns a string
    """
    prompt = comps[random.randint(1,len(comps)-1)]
    int = random.randint(9,12)*0.1
 
    response = openai.Completion.create(
    engine=engine,
    prompt=prompt,
    temperature=int,
    max_tokens=64
    )
    
    return response['choices'][0]['text']

def generateImages():
    """
    Generate an image using the image dataset. Return a string of the path to the image.
    """
    code = int(random.randint(1,10000000)*3.14159)
    imageNumber=random.randint(0,165)
    print(code)

    response = openai.Image.create_variation(
    image=open(f"data/images/img{imageNumber}.png","rb"),
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    img_data = requests.get(image_url).content

    with open(f'data/AIGenImg/image{code}.jpg', 'wb') as f:
        f.write(img_data)

    return f"data/AIGenImg/image{code}.jpg"

# Overloading generateImages() but python doesn't support overloading :(

def generateImages1(input):
    
    code = int(random.randint(1,10000000)*3.14159)
    imageNumber=random.randint(0,165)
    

    response = openai.Image.create(
    prompt=input,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    img_data = requests.get(image_url).content

    with open(f'data/AIGenImg/image{code}.jpg', 'wb') as f:
        f.write(img_data)

    return f"data/AIGenImg/image{code}.jpg"


