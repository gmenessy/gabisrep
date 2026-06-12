from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_ingest_document():
    tenant_id = "test-tenant-1"

    payload = {
        "filename": "test_document.pdf",
        "raw_markdown": "# Test Document",
        "metrics": {
            "original_paragraphs": 10,
            "removed_boilerplate": 2,
            "textrank_retained": 5,
            "simhash_removed": 3
        },
        "tenant_id": tenant_id
    }

    response = client.post(f"/api/v1/dossier/{tenant_id}/documents", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "document_id" in data

    # Check that it's a valid UUID string
    try:
        uuid_obj = uuid.UUID(data["document_id"], version=4)
    except ValueError:
        assert False, f"document_id {data['document_id']} is not a valid UUID"

    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
