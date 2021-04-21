from flask import Flask
from restaurant_matcher.match_service.routes import match_service_blueprint

app = Flask(__name__)
app.register_blueprint(match_service_blueprint)
