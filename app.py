import os
import sys
import csv
import json
import codecs
import random
import requests as rq
from tqdm import tqdm
from PIL import Image
# from InstagramAPI import InstagramAPI
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError
from instagram_private_api import MediaRatios
from instagram_private_api_extensions import media
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

# Tags for Instagram
tags = ['#stars', '#astrophotography', '#telescope', '#physics', '#astronaut', '#blackhole', '#milkyway', '#cosmos', '#solarsystem', '#universe', '#galaxy', '#planets', '#earth', '#mars', '#nasa', '#astrophysics', '#space', '#spacex', '#astronomy', '#moon', '#science', '#cosmology', '#starsigns']

"""
	I have to disable printing on console as
	a module is printing some text that I don't
	need to show.
	Actually, I had to... -_-
"""
def dprint():
	"""
		Disables printing
	"""
	sys.stdout = open(os.devnull, 'w')
# dprint() # Disable Output First

def eprint(value=''):
	"""
		Enables printing
	"""
	sys.stdout = sys.__stdout__
	print(value)
	# dprint()

def to_json(python_object):
	if isinstance(python_object, bytes):
		return {'__class__': 'bytes',
				'__value__': codecs.encode(python_object, 'base64').decode()}
	raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
	if '__class__' in json_object and json_object['__class__'] == 'bytes':
		return codecs.decode(json_object['__value__'].encode(), 'base64')
	return json_object


def onlogin_callback(api, new_settings_file):
	cache_settings = api.settings
	with open(new_settings_file, 'w') as outfile:
		json.dump(cache_settings, outfile, default=to_json)
		print('SAVED: {0!s}'.format(new_settings_file))

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
			eprint(f'{key}: {data[key]}')

	# Download and save image from NASA
	eprint("Downloading Image...")
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
	eprint("Downloading Complete...")

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

	try:
		settings_file = "creds.json"
		if not os.path.isfile(settings_file):
			# settings file does not exist
			eprint('Unable to find file: {0!s}'.format(settings_file))

			# login new
			api = Client(
				insta_name, insta_pass,
				on_login=lambda x: onlogin_callback(x, settings_file))
		else:
			with open(settings_file) as file_data:
				cached_settings = json.load(file_data, object_hook=from_json)
			eprint('Reusing settings: {0!s}'.format(settings_file))

			device_id = cached_settings.get('device_id')
			# reuse auth settings
			api = Client(
				insta_name, insta_pass,
				settings=cached_settings)
			
	except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
		eprint('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

		# Login expired
		# Do relogin but use default ua, keys and such
		api = Client(
			insta_name, insta_pass,
			device_id=device_id,
			on_login=lambda x: onlogin_callback(x, settings_file))

	# Post to Instagram using Private API
	photo_data, photo_size = media.prepare_image(image_location, aspect_ratios=MediaRatios.standard)
	# result = api.post_photo(photo_data, photo_size, caption=caption_data)

if __name__ == '__main__':
	if len(sys.argv) > 3:
		eprint("Pass username and password!")
	else:
		try:
			main(sys.argv[1], sys.argv[2])
			sys.exit(0)
		except KeyboardInterrupt:
			eprint('You choose to exit!')
			sys.exit(0)
		except Exception as e:
			eprint(e)
			sys.exit(1)
