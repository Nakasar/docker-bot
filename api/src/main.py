from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)


@app.route('/info')
def endpointInfo():
    ls = str(subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read())
    args = request.json["args"]
    return jsonify({
        "title": "NO INFO",
        "message": "No informations available for this container.\n" + args
    })


@app.route('/logs')
def endpointLogs():
    return jsonify({
        "title": "NO LOGS",
        "message": "No logs available for this container."
    })


@app.route('/admin')
def endpointAdmin():
    return jsonify({
        "title": "NO ADMIN",
        "message": "No administration available for this container."
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
