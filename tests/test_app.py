import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
import json

def test_health():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

def test_create_page():
    with app.test_client() as client:
        response = client.post('/api/pages', 
            json={'name': 'Homepage'},
            content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Homepage'
        assert response.json['hits'] == 0

def test_increment_hit():
    with app.test_client() as client:
        # Create page
        create_resp = client.post('/api/pages',
            json={'name': 'Test Page'},
            content_type='application/json')
        page_id = create_resp.json['id']
        
        # Increment hit
        hit_resp = client.post(f'/api/pages/{page_id}/hit')
        assert hit_resp.status_code == 200
        assert hit_resp.json['hits'] == 1

def test_metrics_endpoint():
    with app.test_client() as client:
        response = client.get('/metrics')
        assert response.status_code == 200
        assert b'api_requests_total' in response.data

if __name__ == '__main__':
    test_health()
    test_create_page()
    test_increment_hit()
    test_metrics_endpoint()
    print("✓ All tests passed!")