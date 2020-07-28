// const Instagram = require('instagram-web-api');
const Instagram = require('./Instagram')
const FileCookieStore = require('tough-cookie-filestore2');
const fetch = require('node-fetch');

// const username = "astronomyimages";
// const password = "";

const username = process.argv[1];
const password = process.argv[2];

const cookieStore = new FileCookieStore('./cookies.json');
const client = new Instagram({ username, password, cookieStore });

// Nasa API
const api = 'https://api.nasa.gov/planetary/apod/?api_key=NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo';

const getData = async url => {
    try {
        let res = await fetch(url);
        let json = await res.json()
        return json;
    } catch(err) {
        console.log(err);
    }
}

getData(api).then(res => {
    var data = res;
    let credit = '\n\nThis is an auto-generated and auto-published post.The pictures and captions are taken from the NASA API https://api.nasa.gov/. This System is developed by @drreygur using the \'LevPasha/InstagramApi\' unofficial Instagram API.';
    let tags = ['#stars', '#astrophotography', '#telescope', '#physics', '#astronaut', '#blackhole', '#milkyway', '#cosmos', '#solarsystem', '#universe', '#galaxy', '#planets', '#earth', '#mars', '#nasa', '#astrophysics', '#space', '#spacex', '#astronomy', '#moon', '#science', '#cosmology', '#starsigns'];


    var post = async (data) => {
        console.log(data);
        await client.login();

        const photo = data.hdurl;
        let caption = '';

        if (data.title) caption += data.title + '\n\n';
        if (data.explanation) caption += data.explanation + '\n\n';
        if (data.copyright) caption += 'Copyright ' + data.copyright + '\n\n';
        caption += credit + '\n\n';

        let {
            res
        } = await client.uploadPhoto({
            photo,
            caption: caption
        });
        console.log(res);
    }
    post(data);
})