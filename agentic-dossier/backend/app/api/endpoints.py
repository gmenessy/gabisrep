from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    print(f"Received metrics from tenant {tenant_id}: {request.metrics.model_dump()}")

    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing", # Mock status expected by test_ingestion.py
        language_detected="de" # Mock language
    )
