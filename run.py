'''
    Main flask module, load flask application
'''
from app import api_bp
from flask_cors import CORS, cross_origin
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.secret_key = "secretkey"

CORS(app, supports_credentials=True)

app.register_blueprint(api_bp, url_prefix='/machine')

if __name__ == '__main__':
    app.run(debug=True)
