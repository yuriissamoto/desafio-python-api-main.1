from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://'
db = SQLAlchemy()  # db intitialized here
db.init_app(app)


def create_app():
    api = Blueprint('api', __name__)

    # define api routes
    from api.views import lista_despesa, incluir_despesa, health
    api.add_url_rule('/status', 'health', view_func=health, methods=['GET'])
    api.add_url_rule('/despesas', 'lista_despesa', view_func=lista_despesa, methods=['GET'])
    api.add_url_rule('/despesas', 'incluir_despesa', view_func=incluir_despesa, methods=['POST'])

    app.register_blueprint(api, url_prefix='/api')
    return app
