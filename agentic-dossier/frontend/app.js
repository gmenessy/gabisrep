document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('pdf-upload');
    const outputElement = document.getElementById('response-output');

    if (fileInput.files.length === 0) {
        outputElement.textContent = "Please select at least one file to upload.";
        return;
    }

    const tenantId = "default-tenant"; // Mock tenant ID
    outputElement.textContent = `Processing ${fileInput.files.length} file(s)...\n`;

    for (const file of fileInput.files) {
        outputElement.textContent += `\nUploading ${file.name}...\n`;

        // Mocking the CleanDocs pipeline locally
        const dummyMarkdown = `# Document: ${file.name}\n\nThis is a mocked parsed text representation.`;
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

            const data = await response.json();
            console.log("Ingestion response:", data);
            outputElement.textContent += `Success for ${file.name}!\nResponse:\n${JSON.stringify(data, null, 2)}\n`;
        } catch (error) {
            console.error("Error during ingestion:", error);
            outputElement.textContent += `Error processing ${file.name}: ${error.message}\n`;
        }
    }
});
