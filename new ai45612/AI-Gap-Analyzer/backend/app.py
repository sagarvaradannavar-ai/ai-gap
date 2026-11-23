
from pathlib import Path
import sys

# Make the main project folder accessible
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from flask import Flask
from flask_cors import CORS
from backend.routes import api

app = Flask(__name__)

CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

app.register_blueprint(api)

@app.route("/")
def home():
    return "AI Gap Analyzer Backend is Running!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
