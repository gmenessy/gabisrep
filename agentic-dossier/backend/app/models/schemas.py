from typing import Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs before reduction")
    removed_boilerplate: int = Field(..., description="Number of paragraphs removed as boilerplate")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="Name of the uploaded file")
    raw_markdown: str = Field(..., description="Cleaned text from the frontend")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="Generated UUID for the document")
    status: str = Field(..., description="Status of the ingestion ('processing' or 'completed')")
    language_detected: str = Field(..., description="Detected language of the document")
