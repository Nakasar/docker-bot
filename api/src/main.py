from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)


@app.route('/info', methods=["POST"])
def endpointInfo():
    args = request.json["args"]
    containers = str(subprocess.Popen("docker ps", shell=True, stdout=subprocess.PIPE).stdout.read())
    return jsonify({
        "title": "CONTAINERS",
        "message": "Running containers :\n" + containers
    })


@app.route('/logs', methods=["POST"])
def endpointLogs():
    args = request.json["args"]
    return jsonify({
        "title": "NO LOGS",
        "message": "No logs available for this container."
    })


@app.route('/admin', methods=["POST"])
def endpointAdmin():
    return jsonify({
        "title": "NO ADMIN",
        "message": "No administration available for this container."
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
