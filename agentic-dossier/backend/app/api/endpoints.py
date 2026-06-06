from fastapi import APIRouter
from uuid import uuid4
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    print(f"Received document '{request.filename}' for tenant '{tenant_id}'")
    print(f"Metrics: {request.metrics.model_dump()}")

    document_id = uuid4()

    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected="de"
    )
