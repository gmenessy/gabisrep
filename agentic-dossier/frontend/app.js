document.getElementById('submit-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('pdf-upload');
    const outputDiv = document.getElementById('output');

    if (!fileInput.files.length) {
        outputDiv.textContent = "Please select at least one file.";
        return;
    }

    const tenantId = "tenant-123"; // Mock tenant ID

    outputDiv.textContent = "Uploading...";

    for (const file of fileInput.files) {
        console.log(`Processing file: ${file.name}`);

        // Mock CleanDocs pipeline result
        const payload = {
            filename: file.name,
            raw_markdown: `# Dummy Content\nThis is a mock clean document for ${file.name}`,
            metrics: {
                original_paragraphs: 100,
                removed_boilerplate: 20,
                textrank_retained: 50,
                simhash_removed: 30
            },
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
            console.log("Response from server:", data);

            // Create element safely to prevent XSS
            const p = document.createElement('p');
            p.textContent = `Uploaded ${file.name}: Status ${data.status}, ID ${data.document_id}`;
            outputDiv.appendChild(p);

        } catch (error) {
            console.error("Error uploading file:", error);
            const p = document.createElement('p');
            p.textContent = `Error uploading ${file.name}`;
            p.style.color = "red";
            outputDiv.appendChild(p);
        }
    }

    // Clear initial uploading text
    if (outputDiv.firstChild && outputDiv.firstChild.textContent === "Uploading...") {
        outputDiv.removeChild(outputDiv.firstChild);
    }
});
