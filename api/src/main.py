from flask import Flask, jsonify, request
from optparse import OptionParser
from datetime import datetime

from dockerbot import *

app = Flask(__name__)


@app.route('/info', methods=["POST"])
def endpointInfo():
    args = request.json["args"].split(' ')
    if (len(args) == 0):
        # !docker info
        return jsonify({"success": False, "code": "INF-03"})
    parser = OptionParser()
    parser.add_option('-i' , '--images', action='store_true', default=False, dest='about_images')
    parser.add_option('-c' , '--containers', action='store_true', default=False, dest='about_containers')
    (option, remainder) = parser.parse_args(args)
    if (not option.about_images and not option.about_containers):
        # Info must concern either images or containers
        return jsonify({"success": False, "code": "INF-02", "message": "Exacly one of `--images` or `--containers` expected."})
    elif (option.about_containers):
        containersList = containers.listContainers()
        return jsonify({"success": True, "title": "CONTAINERS", "message": "List of running containers:\n" + "\n".join(containersList)})
    elif (option.about_images):
        imagesList = images.listImages()
        return jsonify({"success": True, "title": "IMAGES", "message": "List of local images:\n" + "\n".join(imagesList) + "\n\n_(Other images may be pulled from github or dockerhub)_"})
    else:
        return jsonify({"success": False, "code": "INF-02", "message": "Exacly one of `--images` or `--containers` expected."})


@app.route('/logs', methods=["POST"])
def endpointLogs():
    args = request.json["args"].split(' ')
    if (len(args) == 0):
        return jsonify({"success":False, "code":"LOG-02"})
    parser = OptionParser()
    parser.add_option('-n', '--name', action='store', type='string', default=None, dest='container_name')
    parser.add_option('-l', '--limit', action='store', type='int', default=-1, dest='limit')
    parser.add_option('-e', '--error', action='store_true', default=False, dest='error')
    parser.add_option('--since', type='string', default='01-01/00:00:00', dest='since')
    parser.add_option('--until', type='string', default=datetime.now().strftime('%m-%d/%H:%M:%S'), dest='until')
    (option, remainder) = parser.parse_args(args)
    if (option.container_name is not None):
        return jsonify(logs.listLogs(option.container_name, option.limit, option.error, option.since, option.until))
    else:
        return jsonify({ "success":False, "code":"LOG-02" })


@app.route('/admin', methods=["POST"])
def endpointAdmin():
    """
    Handle requests to /admin endpoint to administrate Docker containers and images.

    Flask requet should contain an "args" key, or admin dashboard will be displayed.
    """
    args = request.json["args"].strip().split(' ')
    if (args[0] == "run" and len(args) == 2):
        result = images.run(args[1])
        if (result["success"]):
            return jsonify({
                "success": True,
                "title": "IMAGE RUNNING",
                "message": result["message"]
            })
        else:
            if (result["code"] == "ADM-11") :
                return jsonify({
                    "success": False,
                    "title": "IMAGE PULLED",
                    "message": result["message"]
                })
            else:
                return jsonify({
                    "success": False,
                    "title": "ERROR",
                    "message": result["message"]
                })
    elif (args[0] == "kill" and len(args) == 2):
        result = containers.kill(args[1])
        if (result["success"]):
            return jsonify({
                "success": True,
                "title": "CONTAINER KILLED",
                "message": result["message"]
            })
        else:
            return jsonify({
                "success": False,
                "title": "ERROR",
                "message": result["message"]
            })
    else:
        return jsonify({
            "success": False,
            "title": "UNKOWN COMMAND",
            "code": "ADM-20",
            "message": "Invalid command parameters for ADMIN."
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
