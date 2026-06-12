from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # Print metrics to console as requested
    print(f"[{tenant_id}] Received document: {request.filename}")
    print(f"Metrics: {request.metrics.model_dump()}")

    # Generate UUID and mock response
    doc_id = uuid.uuid4()

    return DocumentIngestResponse(
        document_id=doc_id,
        status="processing",
        language_detected="de"
    )
