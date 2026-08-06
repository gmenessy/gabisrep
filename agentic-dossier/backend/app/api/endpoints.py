"""
API Endpoints for the Agentic Dossier system.
Contains the REST endpoints for document ingestion.
"""

from fastapi import APIRouter, Path, Body
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(
    tenant_id: str = Path(..., description="The unique identifier of the tenant for data isolation"),
    request: DocumentIngestRequest = Body(..., description="The document ingestion request payload containing cleaned markdown and metrics")
) -> DocumentIngestResponse:
    """
    Ingest a document into the Agentic Dossier.

    This endpoint accepts cleaned markdown text and metrics from the frontend's
    CleanDocs pipeline. It generates a unique document ID and initiates the
    processing pipeline.

    Args:
        tenant_id: Strict data isolation identifier.
        request: The payload containing filename, raw_markdown, metrics, and tenant_id.

    Returns:
        DocumentIngestResponse: The generated document ID, status, and detected language.
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
