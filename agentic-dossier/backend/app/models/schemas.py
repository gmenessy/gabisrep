from pydantic import BaseModel, UUID4
from typing import Dict, Any

class IngestionMetrics(BaseModel):
    original_paragraphs: int
    removed_boilerplate: int
    textrank_retained: int
    simhash_removed: int

class DocumentIngestRequest(BaseModel):
    filename: str
    raw_markdown: str
    metrics: IngestionMetrics
    tenant_id: str

class DocumentIngestResponse(BaseModel):
    document_id: UUID4
    status: str
    language_detected: str
