from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_ingest_document():
    tenant_id = "test-tenant-123"
    payload = {
        "filename": "test_document.pdf",
        "raw_markdown": "# Test Title\n\nThis is a test document.",
        "metrics": {
            "original_paragraphs": 100,
            "removed_boilerplate": 20,
            "textrank_retained": 50,
            "simhash_removed": 30
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
