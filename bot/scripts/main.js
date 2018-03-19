module.exports = function(robot) {
  function apiCall(path, callback) {
    require('request')('http://api:5000' + path, callback);
  }

  /**
    dockerbot listens to channels and responds to its prefix.
  */
  robot.hear(/!docker (.*)/i, function(message) {
    let phrase = message.match[1];
    let [command, ...args] = phrase.split(" ");
    switch (command) {
      case "help":
        helpCommand(message);
        break;
      case "info":
        apiCall("/info?args=" + args.join(" "), (err, res, body) => handleInfoResponse(err, res, body, message))
        break;
      case "logs":
        apiCall("/info?args=" + args.join(" "), (err, res, body) => handleLogsResponse(err, res, body, message))
        break;
      case "admin":
        apiCall("/info?args=" + args.join(" "), (err, res, body) => handleAdminResponse(err, res, body, message))
        break;
      default:
        // Command not recognized.
        robot.messageRoom(message.message.room, {
          channel: message.message.room,
          attachments: [{
            title: "Unknown command",
            text: 'I did not understand what you mean. Type !docker help.',
            color: "#FF0000"
          }]
        });
        break;
    }
  });

  function helpCommand(message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "AIDE",
        text: 'Non implémenté.',
        color: "#0022BB"
      }]
    });
  }

  function handleInfoResponse(err, res, body, message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "DOCKER INFO",
        text: 'Non implémenté.',
        color: "#00BB00"
      }]
    });
  }

  function handleLogsResponse(err, res, body, message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "DOCKER LOGS",
        text: 'Non implémenté.',
        color: "#00BB00"
      }]
    });
  }

  function handleAdminResponse(err, res, body, message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "DOCKER ADMIN",
        text: 'Non implémenté.',
        color: "#00BB00"
      }]
    });
  }
}
