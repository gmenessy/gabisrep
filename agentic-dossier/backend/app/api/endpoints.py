from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest):
    # Verify tenant_id matches the path and request payload if needed

    # Print received metrics to console
    print(f"Received ingestion request for tenant {tenant_id}, file {request.filename}")
    print(f"Metrics: {request.metrics.model_dump()}")

    # Mocking response
    doc_id = uuid.uuid4()

    return DocumentIngestResponse(
        document_id=doc_id,
        status="completed",
        language_detected="de"
    )
