from pydantic import BaseModel, UUID4, Field
from typing import Literal

class IngestionMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original PDF")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="Name of the uploaded PDF file")
    raw_markdown: str = Field(..., description="CleanDocs reduced markdown text")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant ID for data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID4 = Field(..., description="Unique identifier for the ingested document")
    status: Literal["processing", "completed"] = Field(..., description="Current status of the document ingestion")
    language_detected: str = Field(..., description="Detected language of the document")
