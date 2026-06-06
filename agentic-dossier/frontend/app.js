document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const statusArea = document.getElementById('status-area');

    // Default tenant for testing
    const tenantId = 'default-tenant';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        statusArea.innerHTML = ''; // Clear previous status using safe method, here it's just clearing

        const files = fileInput.files;
        if (files.length === 0) {
            statusArea.textContent = 'Please select at least one PDF file.';
            return;
        }

        // Process all selected files
        for (const file of files) {
            const statusLine = document.createElement('p');
            statusLine.textContent = `Processing ${file.name}...`;
            statusArea.appendChild(statusLine);

            // Mock CleanDocs pipeline execution
            const mockPayload = {
                filename: file.name,
                raw_markdown: `# Dummy Markdown for ${file.name}\n\nThis is a mock text reduction.`,
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
                    body: JSON.stringify(mockPayload)
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log('Ingestion response:', data);

                    const successMsg = document.createElement('span');
                    successMsg.style.color = 'var(--color-basil)';
                    successMsg.textContent = ` Success! Doc ID: ${data.document_id}`;
                    statusLine.appendChild(successMsg);
                } else {
                    console.error('Ingestion failed', response.statusText);
                    const errMsg = document.createElement('span');
                    errMsg.style.color = 'red';
                    errMsg.textContent = ` Failed: ${response.statusText}`;
                    statusLine.appendChild(errMsg);
                }
            } catch (error) {
                console.error('Network error during ingestion', error);
                const networkErrMsg = document.createElement('span');
                networkErrMsg.style.color = 'red';
                networkErrMsg.textContent = ` Network Error.`;
                statusLine.appendChild(networkErrMsg);
            }
        }
    });
});
