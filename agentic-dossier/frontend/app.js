document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("pdf-upload");
    const statusMessage = document.getElementById("status-message");

    // Mock tenant ID for now
    const tenantId = "tenant-local-dev";

    uploadBtn.addEventListener("click", async () => {
        const files = fileInput.files;

        if (files.length === 0) {
            statusMessage.textContent = "Please select at least one PDF file.";
            statusMessage.style.backgroundColor = "#F1C400"; // Amarillo
            statusMessage.style.color = "#003A40";
            return;
        }

        statusMessage.textContent = "Processing files...";
        statusMessage.style.backgroundColor = "#f5f7f8";
        statusMessage.style.color = "#003A40";

        for (const file of files) {
            try {
                // 1. Process document locally via CleanDocs pipeline
                const processedDoc = await CleanDocsPipeline.processDocument(file);

                // 2. Prepare payload
                const payload = {
                    filename: processedDoc.filename,
                    raw_markdown: processedDoc.raw_markdown,
                    metrics: processedDoc.metrics,
                    tenant_id: tenantId
                };

                // 3. Send to FastAPI backend
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
                    statusMessage.textContent = `Successfully processed ${file.name}. Document ID: ${result.document_id}`;
                    statusMessage.style.backgroundColor = "#00965E"; // Basil
                    statusMessage.style.color = "white";
                } else {
                    console.error(`Error for ${file.name}:`, response.statusText);
                    statusMessage.textContent = `Error processing ${file.name}: ${response.statusText}`;
                    statusMessage.style.backgroundColor = "red";
                    statusMessage.style.color = "white";
                }
            } catch (error) {
                console.error(`Exception for ${file.name}:`, error);
                statusMessage.textContent = `Exception processing ${file.name}: ${error.message}`;
                statusMessage.style.backgroundColor = "red";
                statusMessage.style.color = "white";
            }
        }
    });
});
