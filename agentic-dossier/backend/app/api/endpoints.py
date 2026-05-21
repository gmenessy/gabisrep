from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
from uuid import uuid4

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    # Print metrics to console
    print(f"Received document from tenant {tenant_id}: {request.filename}")
    print(f"Metrics: {request.metrics.model_dump()}")

    return DocumentIngestResponse(
        document_id=uuid4(),
        status="processing",
        language_detected="de"
    )
