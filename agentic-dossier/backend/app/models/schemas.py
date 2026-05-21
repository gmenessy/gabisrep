from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original PDF")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of paragraphs removed by SimHash due to near-duplicate detection")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="Name of the uploaded file")
    raw_markdown: str = Field(..., description="Cleaned text in Markdown format")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="Unique ID of the ingested document")
    status: str = Field(..., description="Status of the ingestion process")
    language_detected: str = Field(..., description="Detected language of the document")
