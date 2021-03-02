// const Instagram = require('instagram-web-api');
const Instagram = require('./Instagram')
const FileCookieStore = require('tough-cookie-filestore2');
const fetch = require('node-fetch');
const fs = require('fs');
const request = require('request');

// const username = "astronomyimages";
// const password = "";

const username = process.argv[1];
const password = process.argv[2];

const cookieStore = new FileCookieStore('./cookies.json');
const client = new Instagram({ username, password, cookieStore });

// Nasa API
const api = 'https://api.nasa.gov/planetary/apod/?api_key=NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo';

// Download Image
const download = function (uri, filename, callback) {
    request.head(uri, function (err, res, body) {
        request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
    });
};

// Fetch the Image details from NASA api
const getData = async url => {
    try {
        let res = await fetch(url);
        let json = await res.json()
        return json;
    } catch(err) {
        console.log(err);
    }
}


// Do the task
getData(api).then(res => {
    var data = res;
    let credit = '\n\nThis is an auto-generated and auto-published post.The pictures and captions are taken from the NASA API https://api.nasa.gov/. This System is developed by @drreygur';
    /* let tags = [
                "#dailyastronomy", "#astronomy",
                "#space", "#nasa", "#universe", "#astrophotography", "#science", "#cosmos", "#moon", "#stars",
                "#galaxy", "#astrophysics", "#nightsky", "#photography", "#physics", "#milkyway", "#spacex", "#cosmology",
                "#astro", "#earth", "#astronomia", "#sky", "#nature", "#telescope", "#astronaut", "#nightphotography",
                "#solarsystem", "#night", "#planets", "#mars", "#bhfyp"
               ]; */
    
    let mTags = "#astronomy #space #nasa #universe #astrophotography #science #cosmos #moon #stars #galaxy #astrophysics #nightsky #photography #physics #milkyway #spacex #cosmology #astro #earth #astronomia #sky #nature #telescope #astronaut #nightphotography #solarsystem #night #planets #mars #bhfyp"
    
    
//     var mTags = (tags, n) => {
//       tag = "";
//         for(var i=0; i < n; i++) {
//             tag += tags[Math.floor(Math.random() * tags.length)] + " ";
//       }
//         return tag;
//     }

    var post = async (data, tags) => {
        console.log(data);
        await client.login();

        const photo = data.hdurl;
        let caption = '';

        if (data.title) caption += data.title + '\n\n';
        if (data.explanation) caption += data.explanation + '\n\n';
        if (data.copyright) caption += 'Copyright ' + data.copyright + '\n\n';
        caption += credit + '\n\n';
        caption += mTags(tags, 8);

        let {
            res
        } = await client.uploadPhoto({
            photo,
            caption: caption
        });
        console.log(res);
    }

    post(data, tags);

    // let imgExt = data.hdurl.split('.');
    // imgExt = imgExt[imgExt.length - 1];

    // download(data.hdurl, `./Images/${data.date}.${imgExt}`, () => {
    //     console.log('[+] Done!');
    // });
})
