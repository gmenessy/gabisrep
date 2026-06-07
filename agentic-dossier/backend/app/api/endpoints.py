from fastapi import APIRouter
from backend.app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # Print metrics to the console as requested
    print(f"Metrics received for tenant {tenant_id}: {request.metrics.model_dump()}")

    # Mock language detection and return a generated UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
