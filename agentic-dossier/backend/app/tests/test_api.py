from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_ingest_document():
    tenant_id = "tenant123"
    request_data = {
        "filename": "test_doc.pdf",
        "raw_markdown": "# Test Document\n\nThis is a test.",
        "metrics": {
            "original_paragraphs": 10,
            "removed_boilerplate": 2,
            "textrank_retained": 5,
            "simhash_removed": 1
        },
        "tenant_id": tenant_id
    }

    response = client.post(
        f"/api/v1/dossier/{tenant_id}/documents",
        json=request_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"
    assert data["language_detected"] == "de"
    # Ensure document_id is a valid UUID
    assert uuid.UUID(data["document_id"])
