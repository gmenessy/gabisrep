document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('pdf-upload');
    const activityLog = document.getElementById('activity-log');

    const cleanDocs = new CleanDocsPipeline();
    const tenantId = 'tenant_12345'; // Hardcoded tenant ID for Sprint 1 demo

    // Helper to log to UI and console
    function logMessage(msg) {
        console.log(msg);
        const timestamp = new Date().toLocaleTimeString();
        activityLog.textContent += `[${timestamp}] ${msg}\n`;
        activityLog.scrollTop = activityLog.scrollHeight;
    }

    uploadBtn.addEventListener('click', async () => {
        const files = fileInput.files;

        if (files.length === 0) {
            logMessage("Error: Please select at least one PDF file to upload.");
            return;
        }

        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Processing...';

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            logMessage(`\n--- Starting processing for: ${file.name} ---`);

            try {
                // Step 1: Process file locally with CleanDocs (Stub)
                logMessage("Processing document locally via CleanDocs Pipeline...");
                const { raw_markdown, metrics } = await cleanDocs.processDocument(file);
                logMessage(`Local processing complete. Reduced text ready.`);
                logMessage(`Metrics: Original Paragraphs: ${metrics.original_paragraphs}, Retained (TextRank): ${metrics.textrank_retained}, Removed (Boilerplate): ${metrics.removed_boilerplate}, Removed (SimHash): ${metrics.simhash_removed}`);

                // Step 2: Prepare the Request Body
                const requestBody = {
                    filename: file.name,
                    raw_markdown: raw_markdown,
                    metrics: metrics,
                    tenant_id: tenantId
                };

                // Step 3: Send POST Request to FastAPI endpoint
                logMessage("Uploading Cleaned Markdown to Backend...");
                const response = await fetch(`/api/v1/dossier/${tenantId}/documents`, {
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

                // Step 4: Log Response
                logMessage(`Upload Successful! Response Details:`);
                logMessage(`- Document ID: ${responseData.document_id}`);
                logMessage(`- Status: ${responseData.status}`);
                logMessage(`- Detected Language: ${responseData.language_detected}`);

            } catch (error) {
                logMessage(`Error processing ${file.name}: ${error.message}`);
            }
        }

        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload and Process';
        fileInput.value = ''; // Reset file input
    });
});
