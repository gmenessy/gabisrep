from fastapi import APIRouter
from uuid import uuid4
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest):
    """
    Ingest a document from the CleanDocs pipeline.
    """
    # Mock language detection
    language_detected = "de"

    # Print metrics to console
    print(f"[{tenant_id}] Received document: {request.filename}")
    print(f"[{tenant_id}] Metrics: {request.metrics.model_dump()}")

    # Generate UUID
    document_id = uuid4()

    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected=language_detected
    )
