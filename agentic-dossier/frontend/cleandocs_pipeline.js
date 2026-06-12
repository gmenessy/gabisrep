// Mock of the CleanDocs v2 pipeline for Sprint 1
window.mockCleanDocsPipeline = async function(file) {
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 500));

    return {
        filename: file.name,
        markdown: `# Simulated Markdown for ${file.name}\n\nThis is a mocked result of the CleanDocs pipeline processing.`,
        metrics: {
            original_paragraphs: 100,
            removed_boilerplate: 20,
            textrank_retained: 50,
            simhash_removed: 30
        }
    };
};
