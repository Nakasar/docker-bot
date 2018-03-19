from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'hello': 'world'})


@app.route('/rich')
def rich():
    return jsonify({
        'color': '#ff0000',
        'message': 'This message if embeded in red.',
        'title': 'Red Alert'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
