from pydantic import BaseModel, Field
from uuid import UUID
from typing import Dict, Any

class IngestionMetrics(BaseModel):
    original_paragraphs: int
    removed_boilerplate: int
    textrank_retained: int
    simhash_removed: int

class DocumentIngestRequest(BaseModel):
    filename: str
    raw_markdown: str = Field(..., description="The cleaned text from the frontend")
    metrics: IngestionMetrics
    tenant_id: str = Field(..., description="For strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID
    status: str
    language_detected: str
