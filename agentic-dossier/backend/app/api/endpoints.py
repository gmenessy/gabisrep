import uuid
from fastapi import APIRouter
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest) -> DocumentIngestResponse:
    """
    Ingest a new document from the frontend using the CleanDocs v2 pipeline.
    """
    print(f"Received document '{request.filename}' for tenant '{tenant_id}'")
    print(f"Metrics received: {request.metrics.dict()}")

    # Generate a UUID for the document
    document_id = uuid.uuid4()

    # Mocking language detection for now
    language_detected = "de"

    return DocumentIngestResponse(
        document_id=document_id,
        status="processing",
        language_detected=language_detected
    )
