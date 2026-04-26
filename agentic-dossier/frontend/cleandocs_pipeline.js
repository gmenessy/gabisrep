/**
 * Mock of the CleanDocs Pipeline
 * In a real scenario, this would use pdf.js to extract text and apply TextRank/SimHash locally.
 */
async function runCleanDocsPipeline(file) {
    return new Promise((resolve) => {
        // Simulate local processing delay
        setTimeout(() => {
            resolve({
                filename: file.name,
                raw_markdown: `# Cleaned Document: ${file.name}\n\nThis is the simulated reduced text output from the local CleanDocs pipeline.`,
                metrics: {
                    original_paragraphs: Math.floor(Math.random() * 50) + 20,
                    removed_boilerplate: Math.floor(Math.random() * 10) + 1,
                    textrank_retained: Math.floor(Math.random() * 15) + 5,
                    simhash_removed: Math.floor(Math.random() * 5) + 1
                }
            });
        }, 1000);
    });
}
