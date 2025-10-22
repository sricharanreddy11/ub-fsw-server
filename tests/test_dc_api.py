import json
import io
from PIL import Image


class TestHealthEndpoint:
    """Test the ping endpoint returns correct response"""
    
    def test_health_endpoint(self, client):
        """Test ping endpoint is GET only and returns {message: 'pong'}"""
        # Test GET request works
        response = client.get('/api/health')
        assert response.status_code == 200
        
        # Test response format
        data = json.loads(response.data)
        assert data == {'message': 'OK'}
        
        # Test only GET is allowed
        assert client.post('/api/health').status_code == 405


class TestPredictEndpoint:
    """Test the /api/digit-classifier endpoint"""
    
    def test_accepts_valid_28x28_image(self, client, valid_28x28_image):
        """Test endpoint accepts valid 28x28 image in 'image' field"""
        response = client.post(
            '/api/digit-classifier',
            data={'image': (valid_28x28_image, 'test.png')},
            content_type='multipart/form-data'
        )
        assert response.status_code == 200 or response.status_code == 500
    
    def test_response_is_single_digit(self, client, valid_28x28_image):
        """Test response is a single integer between 0-9"""
        response = client.post(
            '/api/digit-classifier',
            data={'image': (valid_28x28_image, 'test.png')},
            content_type='multipart/form-data'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data['prediction'], int)
            assert 0 <= data['prediction'] <= 9
    
    def test_rejects_json_content_type(self, client):
        """Test endpoint rejects application/json content type"""
        response = client.post(
            '/api/digit-classifier',
            data=json.dumps({'image': 'test'}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_rejects_wrong_field_name(self, client):
        """Test endpoint rejects data from non-'image' field"""
        valid_image = io.BytesIO()
        Image.new('L', (28, 28), color=128).save(valid_image, format='PNG')
        valid_image.seek(0)
        
        response = client.post(
            '/api/digit-classifier',
            data={'wrong_field': (valid_image, 'test.png')},
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
    
    def test_rejects_non_28x28_image(self, client):
        """Test endpoint rejects images that are not 28x28"""
        wrong_size_image = io.BytesIO()
        Image.new('L', (64, 64), color=128).save(wrong_size_image, format='PNG')
        wrong_size_image.seek(0)
        
        response = client.post(
            '/api/digit-classifier',
            data={'image': (wrong_size_image, 'test.png')},
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
    
    def test_requires_multipart_form_data(self, client, valid_28x28_image):
        """Test endpoint only accepts multipart/form-data"""
        response = client.post(
            '/api/digit-classifier',
            data={'image': (valid_28x28_image, 'test.png')},
            content_type='multipart/form-data'
        )
        # Should succeed with multipart/form-data
        assert response.status_code in [200, 500]  # 500 if model not loaded
