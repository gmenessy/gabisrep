from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_ingest_document():
    tenant_id = "tenant_test"
    payload = {
        "filename": "test_doc.pdf",
        "raw_markdown": "# Test",
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
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
    # Verify document_id is a valid UUID
    assert uuid.UUID(data["document_id"])
