import pytest
import io
from PIL import Image
import sys
import os
from dotenv import load_dotenv

load_dotenv('.env.test')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Create Flask test app"""
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Flask test client"""
    return app.test_client()

@pytest.fixture
def valid_28x28_image():
    """Create valid 28x28 grayscale image"""
    img = Image.new('L', (28, 28), color=128)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes