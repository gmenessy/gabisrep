document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf-upload');
    const submitBtn = document.getElementById('submit-btn');
    const statusMessage = document.getElementById('status-message');

    // Hardcoded tenant ID for now
    const TENANT_ID = 'default-tenant-123';

    submitBtn.addEventListener('click', async () => {
        const files = fileInput.files;
        if (files.length === 0) {
            statusMessage.textContent = 'Please select at least one PDF file.';
            statusMessage.style.color = 'red';
            return;
        }

        statusMessage.textContent = 'Processing...';
        statusMessage.style.color = 'var(--color-midnight)';

        for (const file of files) {
            try {
                // Mock CleanDocs markdown and metrics extraction
                const mockMarkdown = `# ${file.name}\n\nThis is mock clean markdown text extracted from the PDF.`;
                const mockMetrics = {
                    original_paragraphs: 50,
                    removed_boilerplate: 10,
                    textrank_retained: 20,
                    simhash_removed: 5
                };

                const requestBody = {
                    filename: file.name,
                    raw_markdown: mockMarkdown,
                    metrics: mockMetrics,
                    tenant_id: TENANT_ID
                };

                const response = await fetch(`/api/v1/dossier/${TENANT_ID}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const responseData = await response.json();
                console.log('Ingestion response:', responseData);

                statusMessage.textContent = `Successfully ingested ${file.name}. Document ID: ${responseData.document_id}`;
                statusMessage.style.color = 'var(--color-basil)';
            } catch (error) {
                console.error('Error ingesting document:', error);
                statusMessage.textContent = `Error ingesting ${file.name}: ${error.message}`;
                statusMessage.style.color = 'red';
            }
        }
    });
});
