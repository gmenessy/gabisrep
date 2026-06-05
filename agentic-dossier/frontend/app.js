document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf-upload');
    const submitBtn = document.getElementById('submit-btn');
    const statusContainer = document.getElementById('status-container');

    submitBtn.addEventListener('click', async () => {
        if (!fileInput.files || fileInput.files.length === 0) {
            statusContainer.textContent = "Please select at least one PDF file.";
            return;
        }

        statusContainer.textContent = "Processing files...\n";

        // We use a mock tenant ID for this prototype
        const tenantId = "tenant_123";

        for (const file of fileInput.files) {
            // Sanitize filename for display and transmission
            const sanitizedFilename = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');

            // Mock CleanDocs output
            const mockMarkdown = `# Document: ${sanitizedFilename}\n\nThis is a mocked reduced markdown output from the CleanDocs pipeline.`;
            const mockMetrics = {
                original_paragraphs: 100,
                removed_boilerplate: 20,
                textrank_retained: 50,
                simhash_removed: 30
            };

            const payload = {
                filename: sanitizedFilename,
                raw_markdown: mockMarkdown,
                metrics: mockMetrics,
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
                    console.log(`Success for ${sanitizedFilename}:`, data);
                    statusContainer.textContent += `✓ ${sanitizedFilename}: Processed (ID: ${data.document_id})\n`;
                } else {
                    console.error(`Error for ${sanitizedFilename}: HTTP ${response.status}`);
                    statusContainer.textContent += `✗ ${sanitizedFilename}: Error (HTTP ${response.status})\n`;
                }
            } catch (error) {
                console.error(`Fetch error for ${sanitizedFilename}:`, error);
                statusContainer.textContent += `✗ ${sanitizedFilename}: Network error\n`;
            }
        }
    });
});
