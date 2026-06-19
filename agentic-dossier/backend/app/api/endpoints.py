from fastapi import APIRouter
from uuid import uuid4
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # 1. Print the received metrics to the console
    print(f"Received ingestion request for tenant '{tenant_id}', filename '{request.filename}'")
    print(f"Metrics: {request.metrics.model_dump()}")

    # 2. Mock language detection
    mock_language = "de"

    # 3. Generate UUID
    generated_uuid = uuid4()

    return DocumentIngestResponse(
        document_id=generated_uuid,
        status="processing",
        language_detected=mock_language
    )
