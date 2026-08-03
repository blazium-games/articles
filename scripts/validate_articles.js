import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import {
  ALLOWED_MEDIA_EXT,
  asString,
  checkArticlePath,
  engineArticlesRoot,
  extractLocalMediaPaths,
  isValidSlug,
  loadArticle,
  resolveMediaPath,
  walkMarkdownFiles,
} from './lib/articles.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

async function pathExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const root = engineArticlesRoot(repoRoot);
  const files = await walkMarkdownFiles(root);
  if (files.length === 0) {
    console.error(`No markdown articles found under ${root}`);
    process.exit(1);
  }

  const errors = [];
  const seenSlugs = new Set();
  let deployedCount = 0;

  for (const filePath of files) {
    const article = await loadArticle(filePath, repoRoot);
    const title = asString(article.frontmatter.title);
    const description = asString(article.frontmatter.description);
    const cover = asString(article.frontmatter.cover);
    const slug = article.slug;
    const label = article.relativePath;

    if (!title) errors.push(`${label}: missing frontmatter title`);
    if (!description) errors.push(`${label}: missing frontmatter description`);
    if (!cover) errors.push(`${label}: missing frontmatter cover`);

    if (!slug) {
      errors.push(`${label}: missing required frontmatter slug`);
    } else if (!isValidSlug(slug)) {
      errors.push(
        `${label}: invalid slug "${slug}" (must be kebab-case [a-z0-9-], no spaces)`,
      );
    } else {
      const pathErr = checkArticlePath(filePath, repoRoot, slug);
      if (pathErr) errors.push(`${label}: ${pathErr}`);
      if (seenSlugs.has(slug)) {
        errors.push(`${label}: duplicate slug "${slug}"`);
      }
      seenSlugs.add(slug);
    }

    if (!article.deployed) {
      console.log(`skip media checks (deployed: false): ${label}`);
      continue;
    }

    deployedCount += 1;

    if (cover) {
      const coverPath = resolveMediaPath(article.articleDir, cover);
      if (!(await pathExists(coverPath))) {
        errors.push(`${label}: cover not found: ${cover}`);
      } else {
        const ext = path.extname(coverPath).toLowerCase();
        if (!ALLOWED_MEDIA_EXT.has(ext)) {
          errors.push(`${label}: cover has unsupported extension: ${ext}`);
        }
      }
    }

    for (const media of extractLocalMediaPaths(article.content)) {
      const mediaPath = resolveMediaPath(article.articleDir, media);
      if (!(await pathExists(mediaPath))) {
        errors.push(`${label}: missing media: ${media}`);
        continue;
      }
      const ext = path.extname(mediaPath).toLowerCase();
      if (!ALLOWED_MEDIA_EXT.has(ext)) {
        errors.push(`${label}: unsupported media extension for ${media}: ${ext}`);
      }
    }
  }

  console.log(`Validated ${files.length} articles (${deployedCount} deployed).`);

  if (errors.length) {
    console.error('\nValidation failed:');
    for (const err of errors) console.error(`  - ${err}`);
    process.exit(1);
  }

  console.log('OK');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
