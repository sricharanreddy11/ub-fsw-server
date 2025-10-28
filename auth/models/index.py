from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class VoteSample(db.Model):
    __tablename__ = 'vote_samples'

    id = db.Column(db.Integer,  primary_key=True)
    predicted_label = db.Column(db.Integer, nullable=False)
    true_label = db.Column(db.Integer, nullable=False)
    voted_by = db.Column(db.Integer, db.ForeignKey('users.id') , nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 

    @classmethod
    def create_vote_sample(cls, predicted_label, true_label, voted_by):
        vote_sample = cls(
            predicted_label=predicted_label,
            true_label=true_label,
            voted_by=voted_by
        )
        db.session.add(vote_sample)
        try:
            db.session.commit()
            return vote_sample
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return f'<VoteSample {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'predicted_label': self.predicted_label,
            'true_label': self.true_label,
            'voted_by': self.voted_by,
            'created_at': self.created_at.isoformat()
        }

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    device_id = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'device_id': self.device_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def create_user(cls, user_id, username, device_id=None):
        salt = bcrypt.gensalt()  # In real implementation, hash the password properly
        password_hash = bcrypt.hashpw(device_id.encode('utf-8'), salt).decode('utf-8') # Placeholder password
        user = cls(user_id=user_id, username=username, device_id=device_id, password_hash=password_hash)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
