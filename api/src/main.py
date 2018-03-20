from flask import Flask, jsonify, request
from optparse import OptionParser
import subprocess

import dockerbot.infos.containers
import dockerbot.logs.containers
import dockerbot.admin.images

app = Flask(__name__)

@app.route('/info', methods=["POST"])
def endpointInfo():
    args = request.json["args"]
    containers = dockerbot.infos.containers.listContainers()
    return jsonify({
        "title": "CONTAINERS",
        "message": "Running containers :\n" + "\n".join(containers)
    })

@app.route('/logs', methods=["POST"])
def endpointLogs():
    log_parser = optparse.OptionParser()
    parser.add_option('-n', '--name', action='store', type='string', default=None, dest='container_name')
    parser.add_option('-l', '--limit', action='store', type='int', default=-1, dest='limit')
    parser.add_option('-e', '--error', action='store_true', default=False, dest='error')
    (option, remainder) = log_parser.parse_args(request.json["args"].split(' '))
    if (option.container_name != None)
        return jsonify(dockerbot.logs.containers.listLogs(option.container_name, option.limit, option.error))
    else:
        return jsonify({ "success":False, "code":"LOG-02" })

@app.route('/admin', methods=["POST"])
def endpointAdmin():
    args = request.json["args"].strip().split(' ')
    if (args[0] == "run" and len(args) == 2):
        result = dockerbot.admin.images.run(args[1])
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
    else:
        return jsonify({
            "success": False,
            "title": "RUN COMMAND",
            "message": "No image precised : `!docker admin run <image name>`."
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
