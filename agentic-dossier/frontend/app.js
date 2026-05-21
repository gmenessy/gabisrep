document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const statusMessage = document.getElementById('status-message');
    const responseOutput = document.getElementById('response-output');

    // Default tenant for testing
    const TENANT_ID = 'tenant-123';

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            statusMessage.textContent = 'Please select at least one file.';
            return;
        }

        statusMessage.textContent = 'Processing locally...';
        responseOutput.textContent = '';

        try {
            // Process the first file for now
            const file = files[0];

            // Run the local CleanDocs pipeline
            const processedData = await CleanDocsPipeline.processFile(file);

            // Add tenant ID as required by the schema
            processedData.tenant_id = TENANT_ID;

            statusMessage.textContent = 'Sending to backend...';

            // Send to FastAPI backend
            const response = await fetch(`/api/v1/dossier/${TENANT_ID}/documents`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(processedData)
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const result = await response.json();

            console.log('Ingestion successful:', result);
            statusMessage.textContent = 'Upload complete!';

            // Safely render the response output
            responseOutput.textContent = JSON.stringify(result, null, 2);

        } catch (error) {
            console.error('Error during ingestion:', error);
            statusMessage.textContent = `Error: ${error.message}`;
        }
    });
});
