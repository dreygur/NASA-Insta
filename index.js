const fs = require('fs');
const path = require('path');
const axios = require('axios');
const sharp = require('sharp');
const Instagram = require('instagram-web-api')
const FileCookieStore = require('tough-cookie-filestore2');

// Collect Username and Password from Github's variables as arguments
const username = process.env.INSTAGRAM_USERNAME;
const password = process.env.INSTAGRAM_PASSWORD;

// Saving Cookies for skipping login next time
const cookieStore = new FileCookieStore(path.join('./', 'cookies.json'));
const client = new Instagram({ username, password, cookieStore });

// NASA API
const api = 'https://api.nasa.gov/planetary/apod?api_key=NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo';

/**
 * Image Downloader
 * @param {string} url URL of the image
 * @param {string} filename Name of the file
 */
const download = async ({ uri, filename }) => {
  let res = await axios({
    url: uri,
    method: 'GET',
    responseType: 'stream'
  });

  let location = path.join('./', 'images', filename);

  await res.data.pipe(fs.createWriteStream(location))
    .on('close', err => console.log(err));
};

/**
 * Fetch the Image details from NASA api
 * @param {string} url
 * @returns {Object}
 */
const getData = async url => {
  try {
    let res = await axios.get(url);
    return await res.data;
  } catch (err) {
    return err;
  }
};

;(async () => {
  await client.login()

  getData(api).then(res => {
  var data = res;
  let credit = '\n\nThis is an auto-generated and auto-published post.The pictures and captions are taken from the NASA API https://api.nasa.gov/. This System is developed by @drreygur';
  let mTags = '#astronomy #space #nasa #universe #astrophotography #science #cosmos #moon #stars #galaxy #astrophysics #nightsky #photography #physics #milkyway #spacex #cosmology #astro #earth #astronomia #sky #nature #telescope #astronaut #nightphotography #solarsystem #night #planets #mars #bhfyp';

  var post = async (data, mTags) => {
    await client.login();

    var photo = data.hdurl;
    let caption = '';

    if (data.title) caption += data.title + '\n\n';
    if (data.explanation) caption += data.explanation + '\n\n';
    if (data.copyright) caption += 'Copyright ' + data.copyright + '\n\n';
    caption += credit + '\n\n';
    caption += mTags;

    download({
      uri: photo,
      filename: 'nasa.jpg',
    })

    await sharp(path.join('./', 'images', 'nasa.jpg'))
      .resize(1696, 1064)
      .jpeg({ mozjpeg: true })
      .toBuffer()
      .then(async data => {
          let {res} =  await client.uploadPhoto({
          photo: path.join('./', 'images', 'nasa.jpg'),
          caption
        });
      })
    .catch( err => console.log(err));
  }
  post(data, mTags);
});
})()