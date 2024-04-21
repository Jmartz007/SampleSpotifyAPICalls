from flask import Flask, redirect, url_for, request, render_template, jsonify
import os
import logging
from dotenv import load_dotenv

import SpotifyMain

load_dotenv()

if os.getenv("TEST_ENVIRONMENT") == "TRUE":
    import LoggingUtility
    logger = logging.getLogger('main')
else:
    import LoggingQueueUtility
    logger = logging.getLogger("queue")

print(logger.handlers)
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
    '''
    @app.errorhandler(Exception)
    def custom_exception_logger(e):
        "errorhandler(Exception) will capture all exceptions, use a more specific exception if needed."
        logger.exception("An Exception Occurred")
        return "Custom error page", 500
    '''
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        logger.debug("Loading Home Page")
        return 'Hello, World!'
    
    @app.route('/')
    def root():
        logger.debug("Redirecting to home page")
        return redirect('/home')
    
    @app.route('/home')
    def home_page():
        logger.debug("loading home page")
        return render_template('home.html')
    
    @app.route('/artist_search', methods=["GET", "POST"])
    def artist_search():
        if request.method == "GET":
            logger.debug('Loading Artist Search Page')
            return render_template('ArtistSearch.html')
        if request.method == "POST":
            artistName = request.form['Aname']
            logger.debug(f"searching for artist {artistName}")
            results = SpotifyMain.artist_search(artistName)
            # return redirect(url_for(artist_results(results=results)))
            return results


    @app.route('/artist_results')
    def artist_results(results):
        return results

    return app

