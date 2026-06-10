from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    print(f"Received document ingestion request for tenant {tenant_id}")
    print(f"Metrics: {request.metrics.model_dump()}")

    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="completed",
        language_detected="de"
    )
