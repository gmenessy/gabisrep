import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_document():
    tenant_id = "tenant-test-123"

    payload = {
        "filename": "test_document.pdf",
        "raw_markdown": "# Test\n\nThis is a test document.",
        "metrics": {
            "original_paragraphs": 100,
            "removed_boilerplate": 10,
            "textrank_retained": 20,
            "simhash_removed": 5
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "document_id" in data
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"

def test_ingest_document_invalid_payload():
    tenant_id = "tenant-test-123"

    # Missing required 'metrics' field
    payload = {
        "filename": "test_document.pdf",
        "raw_markdown": "# Test",
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 422
