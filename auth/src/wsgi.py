from gevent import monkey


monkey.patch_all()


from wsgiref.simple_server import WSGIServer

from settings.main import app


def runserver():
    http_server = WSGIServer(
        (app.config.get('APP_HOST'), app.config.get('APP_PORT')),
        app,
        spawn=app.config.get('APP_WORKERS')
    )
    http_server.serve_forever()


if __name__ == '__main__':
    runserver()
