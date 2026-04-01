from pydantic import BaseModel, Field
from uuid import UUID

class DocumentMetrics(BaseModel):
    original_paragraphs: int = Field(..., description="Number of paragraphs in the original document")
    removed_boilerplate: int = Field(..., description="Number of boilerplate paragraphs removed")
    textrank_retained: int = Field(..., description="Number of paragraphs retained by TextRank")
    simhash_removed: int = Field(..., description="Number of duplicate paragraphs removed by SimHash")

class DocumentIngestRequest(BaseModel):
    filename: str = Field(..., description="Original name of the uploaded file")
    raw_markdown: str = Field(..., description="The cleaned markdown text from the CleanDocs pipeline")
    metrics: DocumentMetrics = Field(..., description="Metrics gathered during text reduction")
    tenant_id: str = Field(..., description="Tenant identifier for strict data isolation")

class DocumentIngestResponse(BaseModel):
    document_id: UUID = Field(..., description="Unique identifier generated for the ingested document")
    status: str = Field(..., description="Processing status of the document, e.g., 'processing' or 'completed'")
    language_detected: str = Field(..., description="Detected language of the document")
