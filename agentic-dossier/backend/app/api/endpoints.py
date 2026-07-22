from fastapi import APIRouter, Path
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(
    request: DocumentIngestRequest,
    tenant_id: str = Path(..., description="Tenant ID from URL path")
) -> DocumentIngestResponse:
    # Ensure tenant_id in path matches the request body if needed,
    # though for strict isolation the path is often authoritative.
    # We use path tenant_id for endpoint parameter validation.

    # Mock language detection
    detected_language = "de"

    # Print received metrics to console
    print(f"Received ingestion request for {request.filename} (Tenant: {tenant_id})")
    print(f"Metrics: {request.metrics.model_dump()}")

    # Return mocked response with generated UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected=detected_language
    )
