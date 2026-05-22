from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_ingest_document():
    tenant_id = "test-tenant-123"

    payload = {
        "filename": "test_doc.pdf",
        "raw_markdown": "# Test\nThis is a test document.",
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
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"

    # Verify document_id is a valid UUID
    try:
        uuid_obj = uuid.UUID(data["document_id"])
        assert str(uuid_obj) == data["document_id"]
    except ValueError:
        assert False, "document_id is not a valid UUID"
