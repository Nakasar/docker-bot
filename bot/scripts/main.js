function apiCall(path, callback) {
  robot.http("http://api:5000" + path).get(callback)
}

module.exports = function(robot) {
    robot.respond(/salut/i, function(message) {
        require('request')('http://api:5000', (e, r, b) => {
            if (!e && r.statusCode == 200) {
                message.send(b);
            }
        });
    });

    robot.hear(/alerte/i, function(message) {
      apiCall("/rich", (err, res, body) => {
        if (!e && res.statusCode == 200) {
          robot.adapter.customMessage({
            channel: message.room,
            attachments: [{
              title: body.title,
              text: body.message,
              color: body.color
            }]
          });
        }
      });
    });
}
