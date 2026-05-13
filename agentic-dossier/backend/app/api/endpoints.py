from fastapi import APIRouter
from uuid import uuid4
from ..models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents")
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    print(f"Received metrics: {request.metrics.model_dump()}")

    return DocumentIngestResponse(
        document_id=uuid4(),
        status="processing",
        language_detected="de"
    )
