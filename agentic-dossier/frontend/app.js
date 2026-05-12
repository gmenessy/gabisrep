document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    const fileInput = document.getElementById('pdf-upload');
    const statusContainer = document.getElementById('status-container');

    submitBtn.addEventListener('click', async () => {
        const files = fileInput.files;

        if (files.length === 0) {
            showStatus("Please select at least one file.", "error");
            return;
        }

        // Process each file
        for (const file of files) {
            showStatus(`Processing ${file.name}...`, "info");

            // Mocking CleanDocs pipeline for now
            const mockMarkdown = `# Document: ${file.name}\n\nThis is mock markdown content.`;
            const mockMetrics = {
                original_paragraphs: 100,
                removed_boilerplate: 20,
                textrank_retained: 50,
                simhash_removed: 30
            };

            const tenantId = "default-tenant"; // Mock tenant ID

            const payload = {
                filename: file.name,
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

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log("Server response:", data);
                showStatus(`Success for ${file.name}:\n${JSON.stringify(data, null, 2)}`, "success");
            } catch (error) {
                console.error("Error during ingestion:", error);
                showStatus(`Error for ${file.name}: ${error.message}`, "error");
            }
        }
    });

    function showStatus(message, type) {
        statusContainer.style.display = 'block';
        statusContainer.textContent = message;

        statusContainer.className = ''; // Reset classes
        if (type === 'success') {
            statusContainer.classList.add('status-success');
        } else if (type === 'error') {
            statusContainer.classList.add('status-error');
        }
    }
});
