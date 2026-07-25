from fastapi import APIRouter
from backend.app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    logger.info(f"Received document from tenant {tenant_id}")
    logger.info(f"Metrics: {request.metrics.model_dump()}")

    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
