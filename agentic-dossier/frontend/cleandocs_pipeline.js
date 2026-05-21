/**
 * Mock implementation of the CleanDocs pipeline.
 * In a real scenario, this would use pdf.js to extract text
 * and perform TextRank/SimHash locally in the browser.
 */
class CleanDocsPipeline {
    static async processFile(file) {
        // Mock processing delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        return {
            filename: file.name,
            raw_markdown: `# ${file.name}\n\nThis is a mock cleaned markdown content for the uploaded file.`,
            metrics: {
                original_paragraphs: Math.floor(Math.random() * 100) + 50,
                removed_boilerplate: Math.floor(Math.random() * 20) + 5,
                textrank_retained: Math.floor(Math.random() * 30) + 10,
                simhash_removed: Math.floor(Math.random() * 15) + 2
            }
        };
    }
}
