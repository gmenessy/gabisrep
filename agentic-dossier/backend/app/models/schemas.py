from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import UUID

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs before processing")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of sentences retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="The name of the uploaded file")
    raw_markdown: str = Field(..., description="The cleaned text from the frontend in Markdown format")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Identifier for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="The generated UUID for the ingested document")
    status: str = Field(..., description="Current status of the ingestion process ('processing' or 'completed')")
    language_detected: str = Field(..., description="The language detected in the document")
