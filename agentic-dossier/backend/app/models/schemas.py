"""
Pydantic schemas for the Agentic Dossier API.
Defines the input and output models for document ingestion and processing.
"""

from pydantic import BaseModel, Field
from uuid import UUID


class IngestionMetrics(BaseModel):
    """
    Metrics collected from the CleanDocs pipeline during document ingestion.
    """
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original document")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of duplicate paragraphs removed by SimHash")


class DocumentIngestRequest(BaseModel):
    """
    Request payload for ingesting a document into the system.
    """
    filename: str = Field(..., description="Original filename of the ingested document")
    raw_markdown: str = Field(..., description="The cleaned text from the frontend CleanDocs pipeline")
    metrics: IngestionMetrics = Field(..., description="Metrics from the CleanDocs pipeline")
    tenant_id: str = Field(..., description="Tenant identifier for strict data isolation")


class DocumentIngestResponse(BaseModel):
    """
    Response payload after successfully submitting a document for ingestion.
    """
    document_id: UUID = Field(..., description="Unique identifier generated for the document")
    status: str = Field(..., description="Current status of the ingestion process (e.g., 'processing')")
    language_detected: str = Field(..., description="Detected language of the document (e.g., 'de')")
