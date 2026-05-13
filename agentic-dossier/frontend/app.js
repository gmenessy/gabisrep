document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('pdf-upload');
    const resultsDiv = document.getElementById('results');

    // Use a dummy tenant ID for now
    const tenantId = 'tenant-123';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            alert('Please select at least one PDF file.');
            return;
        }

        resultsDiv.innerHTML = '<p>Processing documents...</p>';

        for (const file of fileInput.files) {
            try {
                // 1. Process document locally (Mocked CleanDocs pipeline)
                console.log(`Processing ${file.name} locally...`);
                const cleanDocsResult = await processWithCleanDocs(file);

                // 2. Prepare payload
                const payload = {
                    filename: file.name,
                    raw_markdown: cleanDocsResult.raw_markdown,
                    metrics: cleanDocsResult.metrics,
                    tenant_id: tenantId
                };

                // 3. Send to backend
                console.log(`Sending ${file.name} to backend...`);
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

                const result = await response.json();
                console.log('Backend response:', result);

                // 4. Update UI
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';

                const fileSpan = document.createElement('span');
                fileSpan.textContent = file.name;

                const contentStr = `<strong>File:</strong> ${fileSpan.outerHTML}<br>
                    <strong>Status:</strong> ${result.status}<br>
                    <strong>Document ID:</strong> ${result.document_id}<br>
                    <strong>Language:</strong> ${result.language_detected}`;

                resultItem.innerHTML = contentStr;
                resultsDiv.appendChild(resultItem);

            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                const errorItem = document.createElement('div');
                errorItem.className = 'result-item';
                errorItem.style.borderLeftColor = 'red';

                const fileSpan = document.createElement('span');
                fileSpan.textContent = file.name;

                errorItem.innerHTML = `<strong>Error processing ${fileSpan.outerHTML}:</strong> ${error.message}`;
                resultsDiv.appendChild(errorItem);
            }
        }

        // Remove the "Processing..." message
        if (resultsDiv.firstChild.tagName === 'P') {
            resultsDiv.removeChild(resultsDiv.firstChild);
        }
    });
});
