from pydantic import BaseModel, Field
from uuid import UUID

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original document")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="Original name of the uploaded file")
    raw_markdown: str = Field(..., description="Cleaned text from the frontend CleanDocs pipeline")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs reduction process")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="Generated unique identifier for the ingested document")
    status: str = Field(..., description="Current status of the ingestion (e.g., 'processing', 'completed')")
    language_detected: str = Field(..., description="Detected language of the document")
