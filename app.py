import os
import sys
import csv
import json
import random
import requests as rq
from tqdm import tqdm
from PIL import Image
from InstagramAPI import InstagramAPI

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
max_width_pf = 1080
max_height_pf = 1350

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

    if src_width > src_height: # Make it vertical
        if src_ratio > 2:
            dst_width, dst_height = 2080, src_height - (src_width - 2080) # Make the ratio as Instagram requires
        else:
            dst_width, dst_height = src_width, src_height # Let them be as they are!
    else: # Make it Horizontal
        dst_width, dst_height = max_width_pf, max_height_pf # Make the ratio as Instagram requires

    # Find the ratio of desired size
    dst_ratio = float(dst_width) / float(dst_height)

    print(f'\nWidth: {src_width}\nHeight: {src_height}\nSource Ratio: {src_ratio}\nTarget Ratio: {dst_ratio}\n')

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

    print("Cropping Success!!!")

def main(insta_name, insta_pass):
    """
        Traditional main() function
    """

    # Get data from NASA-API
    data = rq.get(nasa_uri).json()

    # # Save the retrieved data in json format
    # with open('nasa_data.json', 'a') as nasa:
    #     nasa.write(',' + json.dumps(data, sort_keys=True, indent=4))

    # Save the retrieved data in csv format
    with open('nasa_data.csv', 'a') as nasa:
        d_data = csv.DictWriter(nasa, restval="-", fieldnames=data_locations)
        # d_data.writeheader()
        d_data.writerow(data)

    # Print Some `Magic spells on Terminal`
    for key in data_locations:
        if key in data:
            print(f'{key}: {data[key]}')

    # Download and save image from NASA
    print("Downloading Image...")
    # read 1024 bytes every time
    buffer_size = 1024
    image = rq.get(data['hdurl'], stream=True)
    # get the total file size
    file_size = int(image.headers.get("Content-Length", 0))
    # get the file name
    filename = data['hdurl'].split("/")[-1]
    image_location = f'./images/{data["date"]}.jpg'
    progress = tqdm(image.iter_content(buffer_size), f'Downloading {filename} as {data["date"]}.jpg', total=file_size, unit="B", unit_scale=True)
    with open(image_location, 'wb') as img:
        for i_data in progress:
            img.write(i_data)
            # img.write(image.content)
            progress.update(len(i_data))
    print("Downloading Complete...")

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
    if len(sys.argv) > 3:
        print("Pass username and password!")
    else:
        try:
            main(sys.argv[1], sys.argv[2])
            sys.exit(0)
        except KeyboardInterrupt:
            print('You choose to exit!')
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(1)
