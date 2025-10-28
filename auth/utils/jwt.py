import jwt 
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_default_secret_key")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))


def generate_jwt(user_id, device_id=None):
    payload = {
        "user_id": user_id,
        "device_id": device_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def token_required(f):
    from functools import wraps
    from flask import request, jsonify

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token format is invalid'}), 401
            
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        payload = decode_jwt(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired!'}), 401
        
        return f(payload, *args, **kwargs)

    return decorated