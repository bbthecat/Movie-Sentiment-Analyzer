from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health():
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json().get('ok') is True

def test_analyze_text():
    r = client.post('/api/analyze-text', json={'text':'Great movie!'})
    assert r.status_code == 200
    data = r.json()
    assert 'label' in data and 'score' in data
