import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_document():
    tenant_id = "test_tenant"
    payload = {
        "filename": "test.pdf",
        "raw_markdown": "# Test",
        "metrics": {
            "original_paragraphs": 10,
            "removed_boilerplate": 2,
            "textrank_retained": 5,
            "simhash_removed": 1
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
