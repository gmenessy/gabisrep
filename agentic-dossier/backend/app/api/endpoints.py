from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    """
    Ingests a document to the system.
    """
    # Print metrics to console
    print(f"Received metrics for {request.filename}: {request.metrics.model_dump()}")

    # Mock language detection
    language_detected = "de"

    # Generate UUID
    document_id = uuid.uuid4()

    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected=language_detected
    )
