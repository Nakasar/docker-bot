module.exports = function(robot) {
    function apiCall(path, callback) {
      console.log('Call to: http://api:5000' + path)
      require('request')('http://api:5000' + path, (e, r, b) => {
	callback(e, r, b);
      })
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
	  console.log(message.message.room);
	  console.log(message.rid);
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
