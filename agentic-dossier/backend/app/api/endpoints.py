from fastapi import APIRouter, Path
from app.models.schemas import DocumentIngestRequest, DocumentIngestResponse
import uuid

router = APIRouter()

@router.post("/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(
    request: DocumentIngestRequest,
    tenant_id: str = Path(..., description="Tenant ID for data isolation")
) -> DocumentIngestResponse:
    # Ensure tenant_id in path matches the request payload
    if request.tenant_id != tenant_id:
        # In a real app we might raise an HTTPException
        pass

    # Print the received metrics to the console
    print(f"Received metrics for tenant {tenant_id}: {request.metrics.model_dump()}")

    # Mock language detection and generate a UUID
    return DocumentIngestResponse(
        document_id=uuid.uuid4(),
        status="processing",
        language_detected="de"
    )
