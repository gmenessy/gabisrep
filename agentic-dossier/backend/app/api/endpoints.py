from fastapi import APIRouter
from uuid import uuid4
from ..models.schemas import DocumentIngestRequest, DocumentIngestResponse

router = APIRouter()

@router.post("/api/v1/dossier/{tenant_id}/documents", response_model=DocumentIngestResponse)
async def ingest_document(tenant_id: str, request: DocumentIngestRequest):
    """
    Ingest a document that has been locally processed by the frontend CleanDocs pipeline.
    """
    # Verify that the tenant_id in path matches the request body for safety
    if tenant_id != request.tenant_id:
        # In a real scenario we'd raise HTTPException(status_code=400, detail="Tenant ID mismatch")
        # but for this mock, we'll just continue or could enforce it.
        pass

    # Print the received metrics to the console
    print(f"[{tenant_id}] Received document: {request.filename}")
    print(f"[{tenant_id}] CleanDocs Metrics: {request.metrics.model_dump()}")

    # Generate a UUID for the document
    new_doc_id = uuid4()

    # Return response with mocked language
    return DocumentIngestResponse(
        document_id=new_doc_id,
        status="processing",
        language_detected="de"
    )
