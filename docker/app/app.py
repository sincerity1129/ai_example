from flask import Flask
from flask_restx import Api

from config.basic import server
from route import Auth, Infer

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="Face Swap API Server",
    terms_url="/"
)

api.add_namespace(Auth, '/auth')
api.add_namespace(Infer, '/')

if __name__ == "__main__":
    app.run(host=server['host'], port=server['port'], debug=server['debug'])