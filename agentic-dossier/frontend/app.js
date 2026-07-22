document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("pdf-upload");
    const outputDiv = document.getElementById("output");

    const TENANT_ID = "tenant-local-dev-01"; // Mock tenant ID for now

    uploadBtn.addEventListener("click", async () => {
        const files = fileInput.files;

        if (files.length === 0) {
            outputDiv.textContent = "Please select at least one file.";
            return;
        }

        outputDiv.textContent = "Processing files locally...\n";
        uploadBtn.disabled = true;

        try {
            for (const file of files) {
                // 1. Process locally using the CleanDocs mock pipeline
                outputDiv.textContent += `Processing ${file.name} locally...\n`;
                const { raw_markdown, metrics } = await window.CleanDocsPipeline.processDocument(file);

                // 2. Prepare payload for the backend API
                const payload = {
                    filename: file.name,
                    raw_markdown: raw_markdown,
                    metrics: metrics,
                    tenant_id: TENANT_ID
                };

                // 3. Send securely to the local backend
                outputDiv.textContent += `Sending ${file.name} to ingestion API...\n`;
                const response = await fetch(`/api/v1/dossier/${TENANT_ID}/documents`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    throw new Error(`API error: ${response.status} ${response.statusText}`);
                }

                const result = await response.json();
                console.log("Backend response:", result);

                outputDiv.textContent += `Success: Document ID ${result.document_id}, Status: ${result.status}, Language: ${result.language_detected}\n\n`;
            }
        } catch (error) {
            console.error("Ingestion failed:", error);
            outputDiv.textContent += `\nError during ingestion: ${error.message}`;
        } finally {
            uploadBtn.disabled = false;
        }
    });
});
