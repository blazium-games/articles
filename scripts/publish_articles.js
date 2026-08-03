import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import {
  ARTICLES_PREFIX,
  CDN_BASE,
  asString,
  buildRss,
  engineArticlesRoot,
  extractLocalMediaPaths,
  gitDateForFile,
  loadArticle,
  markdownToBbcode,
  mediaCdnLocation,
  resolveMediaPath,
  rewriteMarkdownMedia,
  walkMarkdownFiles,
} from './lib/articles.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const distRoot = path.join(repoRoot, 'dist', ARTICLES_PREFIX);

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function copyFile(src, dest) {
  await ensureDir(path.dirname(dest));
  await fs.copyFile(src, dest);
}

async function main() {
  const root = engineArticlesRoot(repoRoot);
  const files = await walkMarkdownFiles(root);
  await fs.rm(path.join(repoRoot, 'dist'), { recursive: true, force: true });
  await ensureDir(distRoot);

  /** @type {Array<{slug:string,title:string,description:string,cover:string,date:string,link:string,guid:string}>} */
  const catalog = [];

  for (const filePath of files) {
    const article = await loadArticle(filePath, repoRoot);
    if (!article.deployed) {
      console.log(`skip (deployed: false): ${article.relativePath}`);
      continue;
    }

    const title = asString(article.frontmatter.title);
    const description = asString(article.frontmatter.description);
    const coverRel = asString(article.frontmatter.cover);
    const date = asString(article.frontmatter.date) || gitDateForFile(filePath);
    const slug = article.slug;
    const outDir = path.join(distRoot, slug);
    await ensureDir(outDir);

    const rewriteHref = (href) => {
      if (/^https?:\/\//i.test(href) || href.startsWith('data:') || href.startsWith('mailto:')) {
        return href;
      }
      const abs = resolveMediaPath(article.articleDir, href);
      const loc = mediaCdnLocation(abs, root);
      if (loc) return loc.cdnUrl;
      // Fallback: treat as local asset under this slug
      const cleaned = decodeURIComponent(href.trim()).replace(/\\/g, '/').replace(/^\.\//, '');
      const assetPath = cleaned.includes('/')
        ? cleaned.split('/').filter((p) => p !== '..').join('/')
        : `assets/${path.posix.basename(cleaned)}`;
      return `${CDN_BASE}/${ARTICLES_PREFIX}/${slug}/${assetPath}`;
    };

    const mediaPaths = new Set([
      ...extractLocalMediaPaths(article.content),
      ...(coverRel ? [coverRel] : []),
    ]);

    for (const media of mediaPaths) {
      if (/^https?:\/\//i.test(media) || media.startsWith('data:')) continue;
      const src = resolveMediaPath(article.articleDir, media);
      const loc = mediaCdnLocation(src, root);
      // Only copy files owned by this article folder into its dist tree.
      // Cross-article refs rewrite to the owning slug's CDN URL.
      if (!loc || loc.slug !== slug) continue;
      const dest = path.join(outDir, ...loc.assetRel.split('/'));
      try {
        await copyFile(src, dest);
      } catch (err) {
        throw new Error(`${article.relativePath}: failed to copy media ${media}: ${err.message}`);
      }
    }

    const contentMd = rewriteMarkdownMedia(article.content, rewriteHref);
    const contentBbcode = markdownToBbcode(article.content, rewriteHref);
    const coverUrl = coverRel ? rewriteHref(coverRel) : '';
    const metaLink = `${CDN_BASE}/${ARTICLES_PREFIX}/${slug}/meta.json`;

    const meta = {
      slug,
      title,
      description,
      cover: coverUrl,
      date,
      changes: asString(article.frontmatter.changes) || null,
      link: metaLink,
      content_bbcode: `${CDN_BASE}/${ARTICLES_PREFIX}/${slug}/content.bbcode`,
      content_md: `${CDN_BASE}/${ARTICLES_PREFIX}/${slug}/content.md`,
    };

    await fs.writeFile(path.join(outDir, 'meta.json'), JSON.stringify(meta, null, 2) + '\n', 'utf8');
    await fs.writeFile(path.join(outDir, 'content.md'), contentMd, 'utf8');
    await fs.writeFile(path.join(outDir, 'content.bbcode'), contentBbcode, 'utf8');

    catalog.push({
      slug,
      title,
      description,
      cover: coverUrl,
      date,
      link: metaLink,
      guid: metaLink,
    });

    console.log(`published: ${slug} (${article.relativePath})`);
  }

  catalog.sort((a, b) => {
    if (a.date === b.date) return a.title.localeCompare(b.title);
    return a.date < b.date ? 1 : -1;
  });

  const index = {
    generated_at: new Date().toISOString(),
    count: catalog.length,
    items: catalog,
  };
  await fs.writeFile(path.join(distRoot, 'index.json'), JSON.stringify(index, null, 2) + '\n', 'utf8');
  await fs.writeFile(path.join(distRoot, 'rss.xml'), buildRss(catalog), 'utf8');

  console.log(`Wrote ${catalog.length} articles to ${distRoot}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
