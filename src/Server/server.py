from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "string"


def run_server():
    app.run()
