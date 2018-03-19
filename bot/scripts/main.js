module.exports = function(robot) {
    robot.respond(/salut/i, function(message) {
        require('request')('http://api:5000', (e, r, b) => {
            if (!e && r.statusCode == 200) {
                message.send(b);
            }
        });
    });
}
