var exec = require('child_process').exec;
var fs = require("fs");
var Ivona = require("ivona-node");

var ivona = new Ivona({
	accessKey: 'GDNAJCIHKDP2YAKG664A',
	secretKey: '8yaFb9+jGeuI8DDrYKdK+9jUVNAqqYRuxyG254la'
});

var lookup = {};


function start(message) {
    
    if (lookup[message.speech]) {
        return message.speech
    }

    var sound = ivona.createVoice(message.speech, {
        body: {
            parameters: {
                rate: speech.rate,
                volume: speech.volume,
            },
            voice: {
                name: 'Salli',
                language: 'en-US',
                gender: 'Female'
            }
        }
    }).pipe(fs.createWriteStream(message.speech + '.mp3'));

    if (!sound) {
        //backup MS SAM
    }
}

var player = {
    "name": null, 
    "champion:": null,
    "alive": false,
    "team": 100, // 100 - blue 200 - red
    "participantID": 0,
    "health": 0,
    "mana": 0,
    "armor": 0,
    "ad": 0,
    "ap": 0,
    "items": [],
    "spells": [
        {
            "id": 0,
            "cooldown": 0,
            "level": 0
        },
        {
            "id": 1,
            "cooldown": 0,
            "level": 0
        },
        {
            "id": 2,
            "cooldown": 0,
            "level": 0
        },
        {
            "id": 3,
            "cooldown": 0,
            "level": 0
        },
        {
            "id": 4,
            "cooldown": 0,
            "level": 0
        },
        {
            "id": 5,
            "cooldown": 0,
            "level": 0
        }
    ],
    "kills": 0,
    "deaths": 0,
    "respawn": 0,
    "assists": 0,
    "attackspeed": 0,
    "movement": 0,
    "mr": 0,
    "cs": 0,
    "level": 1,
    "experience": 0,
    "gold": 0
}