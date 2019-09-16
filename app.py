import os
import sys
import json
import random
import requests as rq
from InstagramAPI import InstagramAPI
from PIL import Image

# NASA Details
nasa_api = "https://api.nasa.gov/"
nasa_api_key = "NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo"
nasa_uri = nasa_api + "planetary/apod?api_key=" + nasa_api_key

# Instagram Details
insta_name = ''
insta_pass = ''

# Keys to get exact info from NASA-Dict
data_locations = ["title", "url", "date", "copyright", "hdurl", "explanation", "media_type", "service_version"]

# A Simple Credit Line
credit = '\n\nThis is an auto-generated and auto-published post.The pictures and captions are taken from the NASA API https://api.nasa.gov/. This System is developed by @drreygur using the \'InstagramApi\' unofficial Instagram API.\n\nnInspired from @dailyastronomypicture'

# Instagram required Image measurements
max_width = 1080
max_height = 1350

# Tags for Instagram
tags = ['#stars', '#astrophotography', '#telescope', '#physics', '#astronaut', '#blackhole', '#milkyway', '#cosmos', '#solarsystem', '#universe', '#galaxy', '#planets', '#earth', '#mars', '#nasa', '#astrophysics', '#space', '#spacex', '#astronomy', '#moon', '#science', '#cosmology', '#starsigns']

def main(insta_name, insta_pass):
    """
        Traditional main() function
    """

    # Get data from NASA-API
    data = rq.get(nasa_uri).json()

    # Save the retrieved data in json format
    with open('nasa_data.json', 'a') as nasa:
        nasa.write(json.dumps(data, sort_keys=True, indent=4))

    # Print Some `Magic spells on Terminal`
    for key in data_locations:
        print(f'{key}: {data[key]}')
    
    # Download and save image from NASA
    image = rq.get(data['hdurl'])
    with open(f'{data["date"]}.jpg', 'wb') as img:
        img.write(image.content)

    """
        Here starts the Image resizing Magic
        Code copied from: https://djangosnippets.org/snippets/224/
    """
    img = Image.open(f'./{data["date"]}.jpg')
    
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = max_width, max_height
    dst_ratio = float(dst_width) / float(dst_height)
    
    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = float(src_width - crop_width) / 2
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = float(src_height - crop_height) / 3
    img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
    img = img.resize((dst_width, dst_height), Image.ANTIALIAS)
    img.save(f'./{data["date"]}.jpg')
    # End Magic Code

    # resize = im.crop((x_off, y_off, 600, 600)) #.resize((im.size[0]*5, im.size[1]*4))
    # resize.save(f'./{data["date"]}.jpg')

    # Generate Tags
    tag = ''.join(random.choice(tags) + ' ' for _ in range(7))

    # Post Image to Instagram
    insta = InstagramAPI(insta_name, insta_pass)
    insta.login() # Login to Instagram
    insta.uploadPhoto(f'./{data["date"]}.jpg', caption=f"{data['title']}\n\n{data['explanation']}\n\nCredit: {data['copyright']}\n\n{credit}\n\n{tag}") # Pass Image location and caption

if __name__ == '__main__':
    try:
        # insta_name = str(input('Username: '))
        # insta_pass = str(input('Password: '))
        main(sys.argv[1], sys.argv[2])
    except:
        main(insta_name, insta_pass)
    sys.exit()
