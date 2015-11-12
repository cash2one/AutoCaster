var exec = require('child_process').exec;
var fs = require("fs");
var Ivona = require("ivona-node");

//exec('calc', function (err, stdout, stderr) {
//    console.log(stdout);
//});

var ivona = new Ivona({
	accessKey: 'GDNAJCIHKDP2YAKG664A',
	secretKey: '8yaFb9+jGeuI8DDrYKdK+9jUVNAqqYRuxyG254la'
});

    ivona.createVoice('Kassuhdin got a penta kill.', {
        body: {
            voice: {
                name: 'Salli',
                language: 'en-US',
                gender: 'Female'
            }
        }
    }).pipe(fs.createWriteStream('text.mp3'));