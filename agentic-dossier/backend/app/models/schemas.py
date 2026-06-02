from pydantic import BaseModel, Field
from uuid import UUID

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of original paragraphs before processing")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="The name of the uploaded document")
    raw_markdown: str = Field(..., description="The cleaned Markdown text from the frontend")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="The generated UUID for the ingested document")
    status: str = Field(..., description="Processing status, e.g., 'processing' or 'completed'")
    language_detected: str = Field(..., description="Detected language of the document")
