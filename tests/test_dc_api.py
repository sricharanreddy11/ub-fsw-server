import pytest
import json
from app import app
from auth.models.index import db, VoteSample, User

class TestVotesStatsEndpoint:

    @pytest.fixture(autouse=True)
    def setup(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            user = User.create_user(
                user_id='testuser',
                username='Test User',
                device_id='device123'
            )

            VoteSample.create_vote_sample(predicted_label=3, true_label=3, voted_by=user.id)
            VoteSample.create_vote_sample(predicted_label=5, true_label=2, voted_by=user.id)
            VoteSample.create_vote_sample(predicted_label=3, true_label=3, voted_by=user.id)
        
        yield
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self):
        response = self.client.post('/api/auth/login', json={
            'user_id': 'testuser',
            'username': 'Test User',
            'device_id': 'device123'
        })
        return response.json['token']

    def test_health_check(self):
        response = self.client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'OK'
    
    def test_login(self):
        response = self.client.post('/api/auth/login', json={
            'user_id': 'testuser',
            'username': 'Test User',
            'device_id': 'device123'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
    
    def test_get_votes_distribution(self):
        token = self.get_token()
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.get('/api/digit-classifier/stats', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)

        assert type(data) is list
        assert data[0]['accuracy'] == pytest.approx(2/3)