document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const statusMessage = document.getElementById('status-message');

    // Default tenant for scaffolding
    const tenantId = 'tenant-123';

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            showMessage('Please select at least one file.', 'error');
            return;
        }

        statusMessage.textContent = 'Processing files...';
        statusMessage.className = '';

        let successCount = 0;
        let failCount = 0;

        for (const file of fileInput.files) {
            try {
                // Mock CleanDocs pipeline processing
                const cleanedData = await window.mockCleanDocsPipeline(file);

                // Prepare request payload matching DocumentIngestRequest Pydantic model
                const payload = {
                    filename: cleanedData.filename,
                    raw_markdown: cleanedData.markdown,
                    metrics: cleanedData.metrics,
                    tenant_id: tenantId
                };

                const response = await fetch(`/api/v1/dossier/${tenantId}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log(`Success for ${file.name}:`, data);
                successCount++;
            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                failCount++;
            }
        }

        // Sanitize output by setting textContent instead of innerHTML
        if (failCount === 0) {
            showMessage(`Successfully ingested ${successCount} document(s). Check console for details.`, 'success');
        } else {
            showMessage(`Processed with errors: ${successCount} succeeded, ${failCount} failed.`, 'error');
        }
    });

    function showMessage(text, className) {
        statusMessage.textContent = text;
        statusMessage.className = className;
    }
});
