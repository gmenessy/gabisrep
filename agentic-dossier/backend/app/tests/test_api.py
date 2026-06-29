import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import DocumentIngestRequest, IngestionMetrics

client = TestClient(app)

def test_ingest_document():
    tenant_id = "tenant-test-123"

    payload = {
        "filename": "test_doc.pdf",
        "raw_markdown": "# Test Title\nThis is a test document.",
        "metrics": {
            "original_paragraphs": 100,
            "removed_boilerplate": 10,
            "textrank_retained": 70,
            "simhash_removed": 20
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
