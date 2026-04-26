document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ingest-form');
    const fileInput = document.getElementById('pdf-upload');
    const resultsLog = document.getElementById('results-log');

    // We mock a tenant ID for this scaffold
    const tenantId = 'tenant-demo-123';

    function logToUI(message, type = 'info') {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;

        const timestamp = new Date().toLocaleTimeString();
        entry.textContent = `[${timestamp}] ${message}`;

        resultsLog.appendChild(entry);
        resultsLog.scrollTop = resultsLog.scrollHeight;

        console.log(`[${type.toUpperCase()}] ${message}`);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            logToUI('No files selected.', 'error');
            return;
        }

        for (const file of files) {
            logToUI(`Starting local CleanDocs pipeline for: ${file.name}...`);

            try {
                // 1. Run local mock pipeline
                const processedData = await runCleanDocsPipeline(file);

                logToUI(`CleanDocs finished. Metrics: ${JSON.stringify(processedData.metrics)}`);

                // Prepare payload
                const payload = {
                    filename: processedData.filename,
                    raw_markdown: processedData.raw_markdown,
                    metrics: processedData.metrics,
                    tenant_id: tenantId
                };

                logToUI(`Sending processed payload to backend...`);

                // 2. Send to FastAPI Backend
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

                const responseData = await response.json();

                logToUI(`Success! Server responded: ${JSON.stringify(responseData, null, 2)}`, 'success');

            } catch (error) {
                logToUI(`Error processing ${file.name}: ${error.message}`, 'error');
                console.error(error);
            }
        }

        // Clear input after processing
        form.reset();
    });
});
