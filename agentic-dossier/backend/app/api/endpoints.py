from fastapi import APIRouter, Path, Body
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(
    tenant_id: str,
    request: DocumentIngestRequest
):
    """
    Ingest a document into the Agentic Dossier.
    The text should be reduced and cleaned markdown.
    """
    # Mock language detection
    language_detected = "de"

    # Print metrics to console
    logger.info(f"Received document ingestion request for tenant: {tenant_id}, file: {request.filename}")
    logger.info(f"Ingestion metrics: {request.metrics.model_dump()}")

    # Return generated UUID
    document_id = uuid.uuid4()

    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected=language_detected
    )
