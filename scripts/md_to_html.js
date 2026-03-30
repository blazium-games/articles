import fs from 'fs/promises';
import matter from 'gray-matter';
import { marked } from 'marked';

marked.use({
  renderer: {
    heading({ tokens, depth }) {
      const text = this.parser.parseInline(tokens);
      if (depth > 2) {
        return `<strong>${text}</strong>`;
      } else {
        return `<h${depth+1}>${text}</h${depth+1}>`;
      }
    },
    image({ tokens, href }) {
      return `<strong>[MEDIA:${href}]</strong>`;
    },
  },
});

async function convertMarkdownToHtml(inputPath) {
  try {
    const fileContent = await fs.readFile(inputPath, 'utf8');
    const { data: frontmatter, content: markdownContent } = matter(fileContent);
    const html = marked.parse(markdownContent);
    return { frontmatter, html, rawContent: markdownContent };
  } catch (err) {
    console.error('Error processing markdown:', err.message);
    throw err;
  }
}

(async () => {
  const inputFile = process.argv[2];

  if (!inputFile) {
    console.error('Usage: node md-to-html.js <input.md> [output.html]');
    process.exit(1);
  }

  const result = await convertMarkdownToHtml(inputFile);

  const outputPath = process.argv[3] || inputFile.replace('.md', '.html');
  await fs.writeFile(outputPath, result.html, 'utf8');

  console.log(`Converted successfully! Output: ${outputPath}`);
})();