"""web app"""

from flask import Flask, make_response


def create_app():
    """set up flask"""

    app = Flask(__name__)

    @app.route("/")
    def show_home():
        """Home page"""
        response = make_response("Meow", 200)
        response.mimetype = "text/plain"
        return response

    return app
