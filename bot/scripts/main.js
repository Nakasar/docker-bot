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
        if (args.length == 0 || args[0] === "help") {
          infoHelpCommand(message)
        } else {
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
        }
        break;
      case "logs":
        if (args.length == 0 || args[0] === "help") {
          logsHelpCommand(message);
        } else {
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
        }
        break;
      case "admin":
        if (args.length == 0 || args[0] === "help") {
          adminHelpCommand(message);
        } else {
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
        }
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
    dockerbot listens to channels and responds to message with generic response.
  */
  robot.respond(/(.*)/, function(message) {
    let phrase = message.match[1];
    if (phrase.startsWith("!")) {
      return;
    }
    request({
      baseUrl: apiUrl,
      uri: "/nlp",
      method: "POST",
      json: true,
      body: {
        phrase: phrase
      },
      callback: (err, res, body) => handlePhraseResponse(err, res, body, message)
    });
  });

  /**
    Display help to user (TODO: In Direct Message instead of channel.)
  */
  function helpCommand(message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "HELP",
        color: "#0022BB",
        fields: [
          {
            "short": false,
            "title": "!docker info help",
            "value": "Display informations about containurs or avaialble images."
          },
          {
            "short": false,
            "title": "!docker logs help",
            "value": "Display logs from a given container"
          },
          {
            "short": false,
            "title": "!docker admin help",
            "value": "Administration of containers, images, services..."
          }
        ]
      }]
    });
  }

  /**
    Display help about info command
  */
  function infoHelpCommand(message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "AIDE : INFO",
        text: "`!docker info` command displays informations about containers and images.",
        color: "#0022BB",
        fields: [
          {
            "short": false,
            "title": "!docker info <--images|--container>",
            "value": "List local images or running containers."
          }
        ]
      }]
    });
  }

  /**
    Display help about admin command
  */
  function adminHelpCommand(message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "AIDE : ADMIN",
        text: "`!docker admin` command runs, stop, pause containers.",
        color: "#0022BB",
        fields: [
          {
            "short": false,
            "title": "!docker admin run <image>",
            "value": "Runs the given image if available, pulls it from dockerhub otherwise."
          }
        ]
      }]
    });
  }

  /**
    Display help about logs command
  */
  function logsHelpCommand(message) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: "AIDE : LOGS",
        text: "`!docker logs` Display logs of a running container.",
        color: "#0022BB",
        fields: [
          {
            "short": false,
            "title": "--name <container>",
            "value": "Get the logs from the given container"
          },
          {
            "short": false,
            "title": "--limit <count>",
            "value": "limit to <count> logs displayed"
          },
          {
            "short": false,
            "title": "--since <date>",
            "value": "Get the logs since <date> ( format : Month-Day/Hour:Minutes:Seconds )"
          },
          {
            "short": false,
            "title": "--until <date>",
            "value": "Get the logs until <date> ( format : Month-Day/Hour:Minutes:Seconds )"
          },
          {
            "short": false,
            "title": "--error",
            "value": "Get the logs concerning some error"
          },
        ]
      }]
    });
  }

  /**
    Handle the API response to an "Info" command.
  */
  function handleInfoResponse(err, res, body, message) {
    if (!err && body.success) {
      robot.messageRoom(message.message.room, {
        channel: message.message.room,
        attachments: [{
          title: body.title,
          text: body.message,
          color: "#00BB00"
        }]
      });
    } else if (!err) {
      sendError(message, { title: body.title, error: body.message });
    } else {
      sendError(message);
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
          title: body.title,
          text: body.message,
          color: "#00BB00"
        }]
      });
    } else if (!err) {
      if (body.code == 'LOG-01') sendError(message, {
        error: "The requested container was not found",
        title: "No container found"
      });
      else if (body.code == 'LOG-02') sendError(message, {
        error: "format: !docker logs --name <name> [--limit <limit>] [--error] [--since <date>] [--until <date>] \n"
             + " <name>  : the name of an existing docker image \n"
             + " <limit> : the max count of logs displayed \n"
             + " <date>  : MM-DD/HH:MM/SS",
        title: "Bad format"
      });
    } else {
      sendError(message);
    }
  }

  /**
    Handle the API response to an "Admin" command.
  */
  function handleAdminResponse(err, res, body, message) {
    if (!err && body.success) {
      robot.messageRoom(message.message.room, {
        channel: message.message.room,
        attachments: [{
          title: body.title,
          text: body.message,
          color: "#00BB00"
        }]
      });
    } else if (!err) {
      if (body.code == "ADM-11")  {
        robot.messageRoom(message.message.room, {
          channel: message.room,
          attachments: [{
            title: body.title,
            text: body.message,
            color: "#BB00BB"
          }]
        });
      } else {
        sendError(message, { title: body.title, error: body.message, code: body.code });
      }
    } else {
      sendError(message);
    }
  }

  function handlePhraseResponse(err, res, body, message) {
    if (!err && body.success) {
      robot.messageRoom(message.message.room, {
        channel: message.room,
        attachments: [{
          title: body.title,
          text: body.message,
          color: "#BB00BB"
        }]
      });
    } else if (!err) {
      if (body.code == 'LOG-01') sendError(message, {
        error: "The requested container was not found",
        title: "No container found"
      });
      else if (body.code == 'LOG-02') sendError(message, {
        error: "format: !docker logs --name <name> [--limit <limit>] [--error] [--since <date>] [--until <date>] \n"
             + " <name>  : the name of an existing docker image \n"
             + " <limit> : the max count of logs displayed \n"
             + " <date>  : MM-DD/HH:MM/SS",
        title: "Bad format"
      });
    } else {
      sendError();
    }
  }

  /**
    Send a generic error in response.
    params : errorObject { error: String, title: String, code: String}
  */
  function sendError(message, { error = "An unkown error occured.", title = "ERROR", code = "ERR-00", color = "#FF0000" } = {}) {
    robot.messageRoom(message.message.room, {
      channel: message.message.room,
      attachments: [{
        title: title,
        text: error,
        color: color
      }]
    });
  }
}
