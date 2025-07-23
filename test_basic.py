import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert isinstance(data["short_code"], str)

def test_redirect_to_original_url(client):
    res = client.post("/api/shorten", json={"url": "https://github.com"})
    code = res.get_json()["short_code"]
    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://github.com"

def test_redirect_with_invalid_code(client):
    response = client.get("/invalid123")
    assert response.status_code == 404

def test_url_stats(client):
    res = client.post("/api/shorten", json={"url": "https://python.org"})
    code = res.get_json()["short_code"]
    client.get(f"/{code}")
    stats = client.get(f"/api/stats/{code}")
    assert stats.status_code == 200
    data = stats.get_json()
    assert data["url"] == "https://python.org"
    assert data["clicks"] == 1
    assert "created_at" in data

def test_stats_invalid_code(client):
    response = client.get("/api/stats/nonexistent")
    assert response.status_code == 404
