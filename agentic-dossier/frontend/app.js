document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('pdf-upload');
    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    const tenantId = "default-tenant"; // Hardcoded for now
    const outputDiv = document.getElementById('response-output');
    outputDiv.textContent = "Uploading...\n";

    for (let i = 0; i < fileInput.files.length; i++) {
        const file = fileInput.files[i];

        // Mocking the CleanDocs Markdown generation and metrics
        const dummyMarkdown = `# Dummy Markdown for ${file.name}\n\nThis is a mocked reduction of the PDF text.`;
        const dummyMetrics = {
            original_paragraphs: 100,
            removed_boilerplate: 20,
            textrank_retained: 50,
            simhash_removed: 10
        };

        const payload = {
            filename: file.name,
            raw_markdown: dummyMarkdown,
            metrics: dummyMetrics,
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

            const result = await response.json();
            console.log(`Success for ${file.name}:`, result);
            outputDiv.textContent += `Response for ${file.name}:\n${JSON.stringify(result, null, 2)}\n\n`;
        } catch (error) {
            console.error(`Error for ${file.name}:`, error);
            outputDiv.textContent += `Error for ${file.name}: ${error.message}\n\n`;
        }
    }
});
