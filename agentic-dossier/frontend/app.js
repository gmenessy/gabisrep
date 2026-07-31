document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('pdf-upload');
    const submitBtn = document.getElementById('submit-btn');
    const statusContainer = document.getElementById('status-container');
    const TENANT_ID = 'test-tenant-001'; // Mock tenant ID for now

    submitBtn.addEventListener('click', async () => {
        const files = uploadInput.files;
        if (files.length === 0) {
            alert('Please select at least one PDF file.');
            return;
        }

        statusContainer.textContent = 'Processing files...\n';

        for (const file of files) {
            try {
                // 1. Process document locally using CleanDocs stub
                const cleanDocsData = await window.CleanDocs.processDocument(file);

                // 2. Prepare request payload
                const requestPayload = {
                    filename: file.name,
                    raw_markdown: cleanDocsData.raw_markdown,
                    metrics: cleanDocsData.metrics,
                    tenant_id: TENANT_ID
                };

                // 3. Send POST request to FastAPI backend
                const response = await fetch(`/api/v1/dossier/${TENANT_ID}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestPayload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const responseData = await response.json();
                console.log(`Response for ${file.name}:`, responseData);

                // Update UI safely
                statusContainer.textContent += `✓ ${file.name}: Ingested successfully (ID: ${responseData.document_id})\n`;

            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                statusContainer.textContent += `✗ ${file.name}: Error - ${error.message}\n`;
            }
        }
    });
});
