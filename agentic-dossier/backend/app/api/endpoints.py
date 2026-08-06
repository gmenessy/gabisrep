from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # Print metrics to console
    print(f"Received metrics for tenant {tenant_id}: {request.metrics.model_dump()}")

    # Mock language detection and return generated UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
