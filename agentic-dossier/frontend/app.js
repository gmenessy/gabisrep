document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const pdfUpload = document.getElementById('pdf-upload');
    const statusMessages = document.getElementById('status-messages');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        statusMessages.innerHTML = ''; // clear previous messages

        if (!pdfUpload.files || pdfUpload.files.length === 0) {
            addStatusMessage('Please select at least one file.', true);
            return;
        }

        const tenantId = 'default_tenant';

        for (const file of pdfUpload.files) {
            addStatusMessage(`Processing file: ${file.name}...`);

            // Mock CleanDocs pipeline: generate dummy markdown and metrics
            const payload = {
                filename: file.name,
                raw_markdown: `# Dummy Markdown for ${file.name}\n\nThis is a mock representation of the CleanDocs extracted and reduced text.`,
                metrics: {
                    original_paragraphs: 100,
                    removed_boilerplate: 20,
                    textrank_retained: 30,
                    simhash_removed: 50
                },
                tenant_id: tenantId
            };

            try {
                const response = await fetch(`/api/v1/dossier/${tenantId}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log('Ingestion success:', data);
                    addStatusMessage(`Success for ${file.name}: Document ID ${data.document_id}, Status: ${data.status}`);
                } else {
                    console.error('Ingestion error:', response.statusText);
                    addStatusMessage(`Failed to ingest ${file.name}: ${response.statusText}`, true);
                }
            } catch (error) {
                console.error('Network error during ingestion:', error);
                addStatusMessage(`Network error ingesting ${file.name}.`, true);
            }
        }
    });

    function addStatusMessage(text, isError = false) {
        const p = document.createElement('p');
        p.textContent = text; // Sanitizes input
        if (isError) {
            p.style.borderLeftColor = 'red';
            p.style.backgroundColor = '#ffebee';
        }
        statusMessages.appendChild(p);
    }
});
