from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_document():
    payload = {
        "filename": "test.pdf",
        "raw_markdown": "# Cleaned Text",
        "metrics": {
            "original_paragraphs": 10,
            "removed_boilerplate": 2,
            "textrank_retained": 5,
            "simhash_removed": 1
        },
        "tenant_id": "tenant_123"
    }
    response = client.post("/api/v1/dossier/tenant_123/documents", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
