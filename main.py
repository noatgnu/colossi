import os
import settingmain
import handlers
from tornado import httpserver, ioloop, web

from tornado.options import define, options


define("p", default="9000", help="Backend Listening Port")

settings = {
    "static_path": settingmain.APP_STATIC,
    "cookie_secret": str(os.urandom(45)),
    "debug": True,
    "gzip": True,
    "reload": True,
}

application = web.Application([
    (r"/", handlers.HomeHandler),
    (r"/data/upload", handlers.DataUploadHandler),
    (r"/static", web.StaticFileHandler, {"path": settingmain.APP_STATIC})
], **settings)

if __name__ == "__main__":
    server = httpserver.HTTPServer(application, max_buffer_size=10000000000, max_body_size=100000000000)
    server.listen(options.p)
    ioloop.IOLoop.instance().start()

