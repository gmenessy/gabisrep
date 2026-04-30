from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import UUID

class DocumentIngestMetrics(BaseModel):
    """Metrics from the frontend CleanDocs pipeline."""
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original document")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of sentences retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    """Request model for document ingestion."""
    filename: str = Field(..., description="Name of the uploaded file")
    raw_markdown: str = Field(..., description="Cleaned markdown text from the frontend")
    metrics: DocumentIngestMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for strict data isolation")

class DocumentIngestResponse(BaseModel):
    """Response model for document ingestion."""
    document_id: UUID = Field(..., description="Unique identifier for the ingested document")
    status: str = Field(..., description="Current status of the document processing")
    language_detected: str = Field(..., description="Detected language of the document")
