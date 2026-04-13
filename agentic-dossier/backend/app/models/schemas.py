from pydantic import BaseModel
from typing import Dict
from uuid import UUID

class DocumentIngestMetrics(BaseModel):
    original_paragraphs: int
    removed_boilerplate: int
    textrank_retained: int
    simhash_removed: int

class DocumentIngestRequest(BaseModel):
    filename: str
    raw_markdown: str
    metrics: DocumentIngestMetrics
    tenant_id: str

class DocumentIngestResponse(BaseModel):
    document_id: UUID
    status: str
    language_detected: str
