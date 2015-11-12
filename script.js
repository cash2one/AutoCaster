console.log("WHAT");

var exec = require('child_process').exec;

exec('calc', function (err, stdout, stderr) {
    console.log(stdout);
});