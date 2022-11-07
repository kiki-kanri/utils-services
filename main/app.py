from flask import Blueprint, Flask
from mongoengine import connect

from library.utils import import_attribute


def connect_db(flask_app: Flask):
    connect(**flask_app.config.get('DATABASES')['default'])


def install_apps(flask_app: Flask):
    for app_name in flask_app.config.get('INSTALL_APPS'):
        bps: list[Blueprint] = import_attribute(f'apps.{app_name}.blueprints')

        for bp in bps:
            url_prefix = '/api'

            if bp.url_prefix:
                url_prefix += bp.url_prefix

            flask_app.register_blueprint(bp, url_prefix=url_prefix)


def create_app():
    flask_app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='../templates'
    )

    flask_app.config.from_pyfile('config.py')

    connect_db(flask_app)
    install_apps(flask_app)

    return flask_app
