from digit_classifier.routes.router import digit_classifier_bp
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN', '')
os.environ['HF_USERNAME'] = os.getenv('HF_USERNAME', '')

app = Flask(__name__)
app.register_blueprint(digit_classifier_bp, url_prefix='/api/digit-classifier')

if __name__ == "__main__":
    app.run(debug=True)
