from flask import Flask, redirect, url_for
import os
import logging
from dotenv import load_dotenv

load_dotenv()

if os.getenv("ENVIRONMENT") == "PROD":
    import LoggingQueueUtility
    logger = logging.getLogger("queue")
else:
    import LoggingUtility
    logger = logging.getLogger('main')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    class MyCustomException(Exception):
        '''placeholder for defining a custom exception'''
        pass

    @app.errorhandler(Exception)
    def custom_exception_logger(e):
        '''errorhandler(Exception) will capture all exceptions, use a more specific exception if needed.'''
        logger.exception("An Exception Occurred")
        return "Custom error page", 500

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        logger.debug("Loading Home Page")
        return 'Hello, World!'
    
    @app.route('/')
    def root():
        logger.debug("Redirecting to home page")
        return redirect('/hello')

    return app

