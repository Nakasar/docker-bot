from flask import Flask, jsonify, request
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
    args = request.json["args"].split(' ')
    return jsonify({'success':True, 'data':{ 'title':'fuck', 'message':args.split(' ')}})
    if (len(args) == 4 and '--name' == args[0] and '--limit' == args[2] and args[3].isdigit()):
        return jsonify(dockerbot.logs.containers.listLogs(str(args[1]), int(args[3])))
    elif (len(args) == 2 and '--name' == args[0]):
        return jsonify(dockerbot.logs.containers.listLogs(str(args[1])))
    else:
        return jsonify({ "success":False, "code":"LOG-02" })

@app.route('/admin', methods=["POST"])
def endpointAdmin():
    args = request.json["args"].split(' ')
    if (args[0] == "run" and args.length == 2):
        result = dockerbot.admin.images.run(args[1])
        if (result["success"]):
            return jsonify({
                "title": "IMAGE RUNNING",
                "message": result["message"]
            })
        else:
            if (result["code"] == "ADM-11") :
                return jsonify({
                    "title": "IMAGE PULLED",
                    "message": result["message"]
                })
            else:
                return jsonify({
                    "title": "ERROR",
                    "message": result["message"]
                })
    else:
        return jsonify({
            "title": "RUN COMMAND",
            "message": "No image precised : `!docker admin run <image name>`."
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
