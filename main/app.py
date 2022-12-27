from kikiutils.import_utils import import_attribute
from sanic import Blueprint, Sanic

from .settings import INSTALLED_APPS, MIDDLEWARES, ROOT


def install_apps(sanic_app: Sanic):
    for app_name in INSTALLED_APPS:
        bps: list[Blueprint] = import_attribute(
            f'apps.{app_name}.blueprints'
        )

        for bp in bps:
            url_prefix = '/api'

            if bp.url_prefix:
                url_prefix += bp.url_prefix

            sanic_app.blueprint(bp, url_prefix=url_prefix)

    for rq_middlewares in MIDDLEWARES['request']:
        middleware = import_attribute(rq_middlewares)
        sanic_app.register_middleware(middleware)

    for rp_middlewares in MIDDLEWARES['response']:
        middleware = import_attribute(rp_middlewares)
        sanic_app.register_middleware(middleware, 'response')


def create_app():
    sanic_app = Sanic('SanicApp')
    sanic_app.update_config(ROOT / 'main/settings.py')

    install_apps(sanic_app)

    return sanic_app
