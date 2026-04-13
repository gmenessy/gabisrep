document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('pdf-upload');
    const fileChosen = document.getElementById('file-chosen');
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const resultsContainer = document.getElementById('results');

    // Update file chosen text
    fileUpload.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            if (this.files.length === 1) {
                fileChosen.textContent = this.files[0].name;
            } else {
                fileChosen.textContent = `${this.files.length} files selected`;
            }
        } else {
            fileChosen.textContent = 'No files chosen';
        }
    });

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const files = fileUpload.files;
        if (!files || files.length === 0) {
            addStatusMessage('Please select at least one PDF file.', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        resultsContainer.innerHTML = ''; // Clear previous results

        const tenantId = "tenant-default"; // Hardcoded for this stub

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            addStatusMessage(`Processing ${file.name} (simulated CleanDocs pipeline)...`, 'processing');

            try {
                // Simulate the CleanDocs pipeline processing locally
                const dummyPayload = {
                    filename: file.name,
                    raw_markdown: `# Dummy Markdown for ${file.name}\n\nThis is simulated cleaned text from the CleanDocs pipeline.`,
                    metrics: {
                        original_paragraphs: Math.floor(Math.random() * 100) + 50,
                        removed_boilerplate: Math.floor(Math.random() * 20) + 5,
                        textrank_retained: Math.floor(Math.random() * 30) + 10,
                        simhash_removed: Math.floor(Math.random() * 15) + 2
                    },
                    tenant_id: tenantId
                };

                // Send POST request to FastAPI backend
                const response = await fetch(`/api/v1/dossier/${tenantId}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dummyPayload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                console.log('Backend response:', result);

                addStatusMessage(
                    `Successfully ingested ${file.name}. Document ID: ${result.document_id}, Status: ${result.status}, Lang: ${result.language_detected}`,
                    'success'
                );

            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                addStatusMessage(`Failed to process ${file.name}: ${error.message}`, 'error');
            }
        }

        submitBtn.disabled = false;
        submitBtn.textContent = 'Ingest Documents';
        fileUpload.value = ''; // Reset file input
        fileChosen.textContent = 'No files chosen';
    });

    function addStatusMessage(message, type) {
        const statusDiv = document.createElement('div');
        statusDiv.className = `status-message status-${type}`;
        statusDiv.textContent = message;
        resultsContainer.appendChild(statusDiv);
    }
});
