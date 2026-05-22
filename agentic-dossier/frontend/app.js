document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("pdf-upload");
    const tenantInput = document.getElementById("tenant-id");
    const resultsList = document.getElementById("results-list");

    uploadBtn.addEventListener("click", async () => {
        const files = fileInput.files;
        const tenantId = tenantInput.value.trim();

        if (files.length === 0) {
            alert("Please select at least one PDF file.");
            return;
        }

        if (!tenantId) {
            alert("Please enter a Tenant ID.");
            return;
        }

        for (const file of files) {
            // Mocking CleanDocs Pipeline output
            const mockMarkdown = `# Processed Document: ${file.name}\n\nThis is mock markdown text reduced by 50-70%.`;
            const mockMetrics = {
                original_paragraphs: 42,
                removed_boilerplate: 12,
                textrank_retained: 20,
                simhash_removed: 10
            };

            const payload = {
                filename: file.name,
                raw_markdown: mockMarkdown,
                metrics: mockMetrics,
                tenant_id: tenantId
            };

            try {
                // Post to API Endpoint
                const response = await fetch(`/api/v1/dossier/${encodeURIComponent(tenantId)}/documents`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log("Success:", data);

                // Add result to list securely (avoid XSS)
                const li = document.createElement("li");

                const titleSpan = document.createElement("strong");
                titleSpan.textContent = file.name;

                const resultText = document.createTextNode(` - Processing ID: ${data.document_id} (Language: ${data.language_detected})`);

                li.appendChild(titleSpan);
                li.appendChild(resultText);

                resultsList.appendChild(li);

            } catch (error) {
                console.error("Error uploading file:", file.name, error);
                const li = document.createElement("li");
                li.textContent = `Error processing ${file.name}: ${error.message}`;
                li.style.borderLeftColor = "red";
                resultsList.appendChild(li);
            }
        }
    });
});
