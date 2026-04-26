from pydantic import BaseModel, Field
from uuid import UUID

class CleanDocsMetrics(BaseModel):
    """Metrics from the local frontend CleanDocs pipeline"""
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original PDF")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of near-duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    """Payload sent from the frontend after local processing"""
    filename: str = Field(..., description="Original filename of the PDF")
    raw_markdown: str = Field(..., description="The reduced and cleaned Markdown text")
    metrics: CleanDocsMetrics = Field(..., description="Metrics from the CleanDocs process")
    tenant_id: str = Field(..., description="Identifier for strict data isolation")

class DocumentIngestResponse(BaseModel):
    """Response returned to the frontend after starting the ingestion process"""
    document_id: UUID = Field(..., description="Unique ID generated for the new document")
    status: str = Field(..., description="Status of the ingestion (e.g., 'processing', 'completed')")
    language_detected: str = Field(..., description="Language detected during processing")
