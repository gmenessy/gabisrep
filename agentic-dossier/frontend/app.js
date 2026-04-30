document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const statusMessage = document.getElementById('status-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            statusMessage.textContent = 'Please select at least one file.';
            statusMessage.style.color = 'red';
            return;
        }

        statusMessage.textContent = 'Processing...';
        statusMessage.style.color = 'var(--midnight)';

        // Hardcoded tenant ID for now
        const tenantId = 'tenant-123';

        for (const file of files) {
            try {
                // Mock CleanDocs pipeline response
                const mockPayload = {
                    filename: file.name,
                    raw_markdown: `# Dummy Markdown for ${file.name}\n\nThis is a mock representation of the cleaned text.`,
                    metrics: {
                        original_paragraphs: 50,
                        removed_boilerplate: 10,
                        textrank_retained: 20,
                        simhash_removed: 5
                    },
                    tenant_id: tenantId
                };

                const response = await fetch(`/api/v1/dossier/${tenantId}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(mockPayload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                console.log('Upload successful for', file.name, result);

                statusMessage.textContent = `Successfully processed ${files.length} file(s). Check console for details.`;
                statusMessage.style.color = 'var(--basil)';
            } catch (error) {
                console.error('Error uploading file:', file.name, error);
                statusMessage.textContent = `Error uploading ${file.name}. See console.`;
                statusMessage.style.color = 'red';
            }
        }
    });
});
