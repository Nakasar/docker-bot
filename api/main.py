from flask import Flask
from flask_restful import Resource, Api

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
