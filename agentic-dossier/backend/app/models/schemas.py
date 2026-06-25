from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import UUID

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of original paragraphs in the document")
    removed_boilerplate: int = Field(..., description="Number of paragraphs removed as boilerplate")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="The name of the uploaded file")
    raw_markdown: str = Field(..., description="The cleaned Markdown text from the frontend CleanDocs pipeline")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="The unique identifier for the ingested document")
    status: str = Field(..., description="The status of the ingestion process (e.g., 'processing', 'completed')")
    language_detected: str = Field(..., description="The language detected in the document")
