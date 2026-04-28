from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_ingest_document_success():
    tenant_id = "test_tenant_123"

    request_payload = {
        "filename": "test_document.pdf",
        "raw_markdown": "# Test Document\n\nThis is a mocked test document.",
        "metrics": {
            "original_paragraphs": 10,
            "removed_boilerplate": 2,
            "textrank_retained": 5,
            "simhash_removed": 1
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=request_payload)

    assert response.status_code == 200

    data = response.json()
    assert "document_id" in data
    # Verify document_id is a valid UUID
    assert uuid.UUID(data["document_id"])
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
