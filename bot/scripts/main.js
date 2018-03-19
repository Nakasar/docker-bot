module.exports = function(robot) {
    function apiCall(path, callback) {
      require('request')('http://api:5000' + path, callback);
    }

    robot.respond(/salut/i, function(message) {
        require('request')('http://api:5000', (e, r, b) => {
            if (!e && r.statusCode == 200) {
                message.send(b);
            }
        });
    });

    robot.hear(/alerte/i, function(message) {
      apiCall("/rich", (err, res, body) => {
        if (!err && res.statusCode == 200) {
          let data = JSON.parse(body);
          robot.messageRoom(message.message.room, {
            channel: message.message.room,
            attachments: [{
              title: data.title,
              text: data.message,
              color: data.color
            }]
          });
        }
      });
    });
}
