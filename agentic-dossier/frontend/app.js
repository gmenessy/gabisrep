document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    const fileInput = document.getElementById('pdf-upload');
    const resultsContainer = document.getElementById('results');

    // Hardcoded tenant ID for now
    const tenantId = 'local-tenant-001';

    submitBtn.addEventListener('click', async () => {
        const files = fileInput.files;

        if (files.length === 0) {
            alert('Please select at least one PDF file.');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        resultsContainer.innerHTML = '';

        for (const file of files) {
            try {
                // 1. Process document locally using mock CleanDocs pipeline
                const processedData = await processDocument(file);

                // 2. Prepare payload
                const payload = {
                    filename: file.name,
                    raw_markdown: processedData.raw_markdown,
                    metrics: processedData.metrics,
                    tenant_id: tenantId
                };

                // 3. Send to backend
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
                console.log('Backend response:', responseData);

                // 4. Display result
                const resultElement = document.createElement('div');
                resultElement.className = 'result-item';

                // Safely add content
                const titleElement = document.createElement('strong');
                titleElement.textContent = `File: ${file.name}`;

                const statusElement = document.createElement('p');
                statusElement.textContent = `Status: ${responseData.status} | Lang: ${responseData.language_detected}`;

                const idElement = document.createElement('p');
                idElement.textContent = `Document ID: ${responseData.document_id}`;

                resultElement.appendChild(titleElement);
                resultElement.appendChild(statusElement);
                resultElement.appendChild(idElement);

                resultsContainer.appendChild(resultElement);

            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);

                const errorElement = document.createElement('div');
                errorElement.className = 'result-item';
                errorElement.style.borderLeftColor = 'red';

                const titleElement = document.createElement('strong');
                titleElement.textContent = `Error processing: ${file.name}`;

                const errorTextElement = document.createElement('p');
                errorTextElement.textContent = error.message;

                errorElement.appendChild(titleElement);
                errorElement.appendChild(errorTextElement);

                resultsContainer.appendChild(errorElement);
            }
        }

        submitBtn.disabled = false;
        submitBtn.textContent = 'Process Documents';
        fileInput.value = ''; // clear input
    });
});
