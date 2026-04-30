from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    """
    Ingest a document from the frontend CleanDocs pipeline.
    """
    # Print the received metrics to the console
    print(f"Received metrics for tenant {tenant_id}: {request.metrics.model_dump()}")

    # Mock the language detection and return a generated UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
