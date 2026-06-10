// Mock CleanDocs v2 Pipeline
async function processDocument(file) {
    console.log(`Processing file: ${file.name} through CleanDocs pipeline...`);

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock markdown and metrics
    return {
        raw_markdown: `# CleanDocs Output for ${file.name}\n\nExtracted and reduced text content goes here.`,
        metrics: {
            original_paragraphs: Math.floor(Math.random() * 50) + 10,
            removed_boilerplate: Math.floor(Math.random() * 5) + 1,
            textrank_retained: Math.floor(Math.random() * 20) + 5,
            simhash_removed: Math.floor(Math.random() * 10) + 2
        }
    };
}
