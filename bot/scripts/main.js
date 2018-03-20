const request = require('request');
const apiUrl = "http://api:5000";

module.exports = function(robot) {

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
        request({
          baseUrl: apiUrl,
          uri: "/info",
          method: "POST",
          json: true,
          body: {
            args: args.join(" ")
          },
          callback: (err, res, body) => handleInfoResponse(err, res, body, message)
        });
        break;
      case "logs":
        request({
          baseUrl: apiUrl,
          uri: "/logs",
          method: "POST",
          json: true,
          body: {
            args: args.join(" ")
          },
          callback: (err, res, body) => handleLogsResponse(err, res, body, message)
        });
        break;
      case "admin":
        request({
          baseUrl: apiUrl,
          uri: "/admin",
          method: "POST",
          json: true,
          body: {
            args: args.join(" ")
          },
          callback: (err, res, body) => handleAdminResponse(err, res, body, message)
        });
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

  /**
    Display help to user (TODO: In Direct Message instead of channel.)
  */
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

  /**
    Handle the API response to an "Info" command.
  */
  function handleInfoResponse(err, res, body, message) {
    if (err) {
      sendError(message, { error: "Une erreur inconue est survenue."});
    } else {
      robot.messageRoom(message.message.room, {
        channel: message.message.room,
        attachments: [{
          title: body.title,
          text: body.message,
          color: "#00BB00"
        }]
      });
    }
  }

  /**
    Handle the API response to a "logs" command.
  */
  function handleLogsResponse(err, res, body, message) {
    if (!err && body.success) {
      robot.messageRoom(message.message.room, {
        channel: message.message.room,
        attachments: [{
          title: body.data.title,
          text: body.data.message,
          color: "#00BB00"
        }]
      });
    } else if (!err) {
      if (body.code == 'LOG-01') sendError(message, {
        error = "The requested container was not found",
        title = "No container found"
      });
      else if (body.code == 'LOG-02') sendError(message, {
        error = "format: !docker logs --name <name> [--limit <limit>]",
        title = "Bad format"
      });
    } else {
      sendError(message);
    }
  }

  /**
    Handle the API response to an "Admin" command.
  */
  function handleAdminResponse(err, res, body, message) {
    sendError(message, { error: "Une erreur inconue est survenue en lançant l'administration du container.", title: "Oups :'(" });
  }

  /**
    Send a generic error in response.
    params : errorObject { error: String, title: String, code: String}
  */
  function sendError(message, { error = "Une erreur inconnue est survenue.", title = "Erreur", code = "ERR-00" } = {}) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: title,
        text: error,
        color: "#FF0000"
      }]
    });
  }
}
