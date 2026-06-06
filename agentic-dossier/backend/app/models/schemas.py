from pydantic import BaseModel
from uuid import UUID
from typing import Literal

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
    document_id: UUID
    status: Literal["processing", "completed"]
    language_detected: str
