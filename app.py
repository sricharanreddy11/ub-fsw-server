from digit_classifier.routes.router import digit_classifier_bp
from auth.router.index import auth_bp
from flask import Flask, jsonify
from dotenv import load_dotenv
from auth.models.index import db
import os
from flask_cors import CORS


load_dotenv()

os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN', '')
os.environ['HF_USERNAME'] = os.getenv('HF_USERNAME', '')

app = Flask(__name__)
CORS(app, origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(digit_classifier_bp, url_prefix='/api/digit-classifier')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'message': 'OK'}), 200

if __name__ == "__main__":
    app.run(debug=True)
