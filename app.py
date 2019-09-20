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
# insta_name = ''
# insta_pass = ''

# Keys to get exact info from NASA-Dict
data_locations = ["title", "url", "date", "copyright", "hdurl", "explanation", "media_type", "service_version"]

# A Simple Credit Line
credit = '\n\nThis is an auto-generated and auto-published post.The pictures and captions are taken from the NASA API https://api.nasa.gov/. This System is developed by @drreygur using the \'LevPasha/InstagramApi\' unofficial Instagram API.'

# Instagram required Image measurements
max_width = 1080
max_height = 1350

# Tags for Instagram
tags = ['#stars', '#astrophotography', '#telescope', '#physics', '#astronaut', '#blackhole', '#milkyway', '#cosmos', '#solarsystem', '#universe', '#galaxy', '#planets', '#earth', '#mars', '#nasa', '#astrophysics', '#space', '#spacex', '#astronomy', '#moon', '#science', '#cosmology', '#starsigns']

def img_resize(image_location):
    """
        Here starts the Image resizing Magic
        Code copied from: https://djangosnippets.org/snippets/224/
    """

    img = Image.open(image_location)
    # img = Image.open('K218b_ESAKornmesser_6000' + '.jpg')

    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)

    if src_width > src_height:
        # dst_width, dst_height = max_height, max_width
        dst_width, dst_height = 2080, 1080
    else:
        dst_width, dst_height = max_width, max_height

    dst_ratio = float(dst_width) / float(dst_height)

    # print(src_width, src_height, dst_width, dst_height, src_ratio, dst_ratio)
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
    img.save(image_location)
    # End Magic Code

    # resize = im.crop((x_off, y_off, 600, 600)) #.resize((im.size[0]*5, im.size[1]*4))
    # resize.save(f'./{data["date"]}.jpg')

def save_image_location(date='', url='', hdurl=''):
    with open('raw_images.txt', 'a') as location:
        location.write(f'Date: {date}\n\tUrl: {url}\n\tHD_url: {hdurl}\n\n')

def main(insta_name, insta_pass):
    """
        Traditional main() function
    """

    # Get data from NASA-API
    data = rq.get(nasa_uri).json()

    # Save the retrieved data in json format
    with open('nasa_data.json', 'a') as nasa:
        nasa.write(json.dumps(data, sort_keys=True, indent=4))

    # Save Image Links to a Text file for future use
    save_image_location(data['date'], data['url'], data['hdurl'])

    # Print Some `Magic spells on Terminal`
    for key in data_locations:
        if key in data:
            print(f'{key}: {data[key]}')

    # Download and save image from NASA
    image = rq.get(data['hdurl'])
    image_location = f'./images/{data["date"]}.jpg'
    with open(image_location, 'wb') as img:
        img.write(image.content)

    # Resize the downloaded image
    img_resize(image_location)

    # Generate Tags
    tag = ''.join(random.choice(tags) + ' ' for _ in range(7))

    # Caption for the post
    caption_data = ''
    if 'title' in data:
        caption_data += data['title'] + '\n\n'
    if 'explanation' in data:
        caption_data += data['explanation'] + '\n\n'
    if 'copyright' in data:
        caption_data += 'Copyright: ' + data['copyright'] + '\n\n'
    caption_data += credit + '\n\n' + tag

    # Post Image to Instagram
    insta = InstagramAPI(insta_name, insta_pass)
    insta.login() # Login to Instagram
    insta.uploadPhoto(image_location, caption=caption_data) # Pass Image location and caption

if __name__ == '__main__':
    # img_resize(data={'date': '2019-09-17'})
    try:
        main(sys.argv[1], sys.argv[2])
        sys.exit(0)
    except KeyboardInterrupt:
        print('You choose to exit!')
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
