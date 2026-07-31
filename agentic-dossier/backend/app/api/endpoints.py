from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # Print the received metrics to the console using logging
    logger.info(f"Received metrics for tenant {tenant_id}: {request.metrics.model_dump()}")

    # Mock language detection and return generated UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
