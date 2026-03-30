/**
 * Agentic Dossier - Frontend Application Stub
 */

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const statusMessage = document.getElementById('status-message');
    const consoleOutput = document.getElementById('console-output');

    // Tenant ID for data isolation - mock value for this stub
    const MOCK_TENANT_ID = 'tenant_12345';

    function logToConsole(message, data = null) {
        let text = message;
        if (data) {
            text += '\n' + JSON.stringify(data, null, 2);
        }
        console.log(text);

        const timestamp = new Date().toLocaleTimeString();
        consoleOutput.textContent = `[${timestamp}] ${text}\n` + consoleOutput.textContent;
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            statusMessage.textContent = 'Please select at least one file.';
            return;
        }

        const files = Array.from(fileInput.files);
        statusMessage.textContent = `Processing ${files.length} file(s)...`;
        logToConsole(`Starting upload for ${files.length} file(s)`);

        for (const file of files) {
            try {
                logToConsole(`Mocking CleanDocs pipeline for file: ${file.name}...`);

                // Mocking the CleanDocs markdown generation and metrics
                const mockCleanedMarkdown = `# ${file.name}\n\nThis is mocked text that represents the output of the CleanDocs pipeline locally processing the PDF.`;
                const mockMetrics = {
                    original_paragraphs: Math.floor(Math.random() * 50) + 10,
                    removed_boilerplate: Math.floor(Math.random() * 10) + 2,
                    textrank_retained: Math.floor(Math.random() * 20) + 5,
                    simhash_removed: Math.floor(Math.random() * 5)
                };

                const requestBody = {
                    filename: file.name,
                    raw_markdown: mockCleanedMarkdown,
                    metrics: mockMetrics,
                    tenant_id: MOCK_TENANT_ID
                };

                logToConsole(`Sending POST request for ${file.name} to /api/v1/dossier/${MOCK_TENANT_ID}/documents`);

                const response = await fetch(`/api/v1/dossier/${MOCK_TENANT_ID}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const responseData = await response.json();
                logToConsole(`Success for ${file.name}:`, responseData);

            } catch (error) {
                console.error('Upload failed:', error);
                logToConsole(`Error uploading ${file.name}: ${error.message}`);
                statusMessage.textContent = 'Upload failed. See console for details.';
            }
        }

        statusMessage.textContent = 'All selected files processed.';
        // Reset file input
        fileInput.value = '';
    });
});
