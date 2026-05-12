from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    print(f"Received document ingestion request for tenant: {tenant_id}")
    print(f"Filename: {request.filename}")
    print(f"Metrics: {request.metrics.model_dump()}")

    document_id = uuid.uuid4()

    # Mocking language detection and processing status
    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected="de"
    )
