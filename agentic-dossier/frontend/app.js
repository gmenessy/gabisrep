document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf-upload');
    const submitBtn = document.getElementById('submit-btn');
    const outputDiv = document.getElementById('output');

    submitBtn.addEventListener('click', async () => {
        const files = fileInput.files;
        if (files.length === 0) {
            outputDiv.textContent = "Please select at least one file.";
            return;
        }

        const tenantId = "tenant-12345"; // Sample tenant ID
        let outputText = "Processing started...\n\n";
        outputDiv.textContent = outputText;

        for (const file of files) {
            // Mocking CleanDocs v2 pipeline
            const mockMarkdown = `# ${file.name}\n\nThis is a mock markdown output of the cleaned PDF.`;
            const mockMetrics = {
                original_paragraphs: 100,
                removed_boilerplate: 20,
                textrank_retained: 30,
                simhash_removed: 10
            };

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

                if (response.ok) {
                    const result = await response.json();
                    console.log(`Success for ${file.name}:`, result);
                    outputText += `Successfully processed ${file.name}.\n`;
                    outputText += `Response: ${JSON.stringify(result, null, 2)}\n\n`;
                } else {
                    console.error(`Error for ${file.name}:`, response.statusText);
                    outputText += `Failed to process ${file.name}: ${response.statusText}\n\n`;
                }
            } catch (error) {
                console.error(`Network error for ${file.name}:`, error);
                outputText += `Network error for ${file.name}: ${error.message}\n\n`;
            }

            // Use textContent to avoid XSS
            outputDiv.textContent = outputText;
        }
    });
});
