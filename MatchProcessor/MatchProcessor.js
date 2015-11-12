var program = require('commander');
var util = require('util');
var https = require('https');

var region = "na";
var host = util.format("https://%s.api.pvp.net", region);
var getMatchEndpoint = util.format("/api/lol/%s/v2.2/match/", region);

program
	.version('0.0.1')
	.option('-m, --match <n>', "Match Id", parseInt)
  .option('-k, --api-key <s>', "Api Key")
	.parse(process.argv);

if (program.apiKey === undefined) {
  console.error("API Key not specified");
  return;
}

if (program.match === undefined) {
	console.error("No match id provided.");
	return;
}

var matchEndpoint = host + getMatchEndpoint + program.match + "?includeTimeline=true&api_key=" + program.apiKey;
var timelineDataString = "";

https.get(matchEndpoint, function(res) {
  res.setEncoding('utf8');
  res.on('data', function(data) {
  	timelineDataString += data;
  });
  res.on('end', function() {
    var timelineData = JSON.parse(timelineDataString);
    console.log(JSON.stringify(timelineData));
  });
});
