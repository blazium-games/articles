import fs from 'fs/promises';
import path from 'path';
import { execFileSync } from 'child_process';
import matter from 'gray-matter';

export const CDN_BASE = 'https://cdn.blazium.app';
export const ARTICLES_PREFIX = 'articles';
export const ENGINE_DIR = 'engine';
/** kebab-case, no spaces: a-z, 0-9, hyphens */
export const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
export const ALLOWED_MEDIA_EXT = new Set(['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']);

/** @param {string} repoRoot */
export function engineArticlesRoot(repoRoot) {
  return path.join(repoRoot, ENGINE_DIR);
}

/**
 * @param {string} name
 * @returns {string}
 */
export function slugify(name) {
  return name
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * @param {string} slug
 * @returns {boolean}
 */
export function isValidSlug(slug) {
  return typeof slug === 'string' && SLUG_PATTERN.test(slug) && !/\s/.test(slug);
}

/**
 * @param {string} dir
 * @returns {Promise<string[]>}
 */
export async function walkMarkdownFiles(dir) {
  const out = [];
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch (err) {
    if (err && err.code === 'ENOENT') return out;
    throw err;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await walkMarkdownFiles(full)));
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) {
      out.push(full);
    }
  }
  return out.sort();
}

/**
 * @param {string} href
 * @returns {string}
 */
export function decodeMediaHref(href) {
  const trimmed = href.trim();
  try {
    return decodeURIComponent(trimmed);
  } catch {
    return trimmed;
  }
}

/**
 * @param {string} markdown
 * @returns {string[]}
 */
export function extractLocalMediaPaths(markdown) {
  const found = new Set();
  const mdImg = /!\[[^\]]*]\(([^)]+)\)/g;
  const htmlImg = /<img[^>]+src=["']([^"']+)["']/gi;
  let m;
  while ((m = mdImg.exec(markdown)) !== null) {
    found.add(m[1].trim());
  }
  while ((m = htmlImg.exec(markdown)) !== null) {
    found.add(m[1].trim());
  }
  return [...found].filter((p) => p && !/^https?:\/\//i.test(p) && !p.startsWith('data:') && !p.startsWith('mailto:'));
}

/**
 * Resolve a local media href against an article directory.
 * @param {string} articleDir
 * @param {string} href
 * @returns {string} absolute filesystem path
 */
export function resolveMediaPath(articleDir, href) {
  return path.resolve(articleDir, decodeMediaHref(href));
}

/**
 * Given an absolute media path under the engine articles root, return CDN URL
 * under the owning article slug (folder name), or null if outside root.
 * @param {string} absMediaPath
 * @param {string} engineRoot
 * @returns {{ slug: string, assetRel: string, cdnUrl: string } | null}
 */
export function mediaCdnLocation(absMediaPath, engineRoot) {
  const rel = path.relative(engineRoot, absMediaPath);
  if (!rel || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  const parts = rel.split(path.sep);
  if (parts.length < 2) return null;
  const slug = parts[0];
  if (!isValidSlug(slug)) return null;
  const assetRel = parts.slice(1).join('/');
  return {
    slug,
    assetRel,
    cdnUrl: `${CDN_BASE}/${ARTICLES_PREFIX}/${slug}/${assetRel}`,
  };
}

/**
 * Expected layout: engine/<slug>/<slug>.md
 * @param {string} filePath
 * @param {string} repoRoot
 * @param {string} slug
 * @returns {string|null} error message or null if ok
 */
export function checkArticlePath(filePath, repoRoot, slug) {
  const rel = path.relative(repoRoot, filePath).replace(/\\/g, '/');
  const expected = `${ENGINE_DIR}/${slug}/${slug}.md`;
  if (rel !== expected) {
    return `path must be ${expected} (got ${rel})`;
  }
  return null;
}

/**
 * @param {string} filePath
 * @param {string} repoRoot
 */
export async function loadArticle(filePath, repoRoot) {
  const raw = await fs.readFile(filePath, 'utf8');
  const { data, content } = matter(raw);
  const articleDir = path.dirname(filePath);
  const folderName = path.basename(articleDir);
  const slugRaw = asString(data.slug);
  const slug = slugRaw;
  const deployed = data.deployed === true || data.deployed === 'true';
  return {
    filePath,
    articleDir,
    folderName,
    slug,
    deployed,
    frontmatter: data,
    content,
    relativePath: path.relative(repoRoot, filePath).replace(/\\/g, '/'),
  };
}

/**
 * @param {string} filePath
 * @returns {string} YYYY-MM-DD
 */
export function gitDateForFile(filePath) {
  try {
    const out = execFileSync(
      'git',
      ['log', '-1', '--format=%cs', '--', filePath],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] },
    ).trim();
    if (/^\d{4}-\d{2}-\d{2}$/.test(out)) return out;
  } catch {
    // fall through
  }
  return new Date().toISOString().slice(0, 10);
}

/**
 * @param {unknown} value
 * @returns {string}
 */
export function asString(value) {
  if (typeof value === 'string') return value.trim();
  if (value == null) return '';
  return String(value).trim();
}

/**
 * Minimal Markdown → BBCode for Hub RichTextLabel.
 * @param {string} markdown
 * @param {(href: string) => string} rewriteHref
 */
export function markdownToBbcode(markdown, rewriteHref) {
  let text = markdown.replace(/\r\n/g, '\n');

  // Fenced code blocks
  text = text.replace(/```[\w]*\n([\s\S]*?)```/g, (_m, code) => {
    return `[code]${code.trimEnd()}[/code]`;
  });

  // Images ![alt](src)
  text = text.replace(/!\[([^\]]*)]\(([^)]+)\)/g, (_m, alt, src) => {
    const href = rewriteHref(src.trim());
    const label = alt ? String(alt) : '';
    return label ? `[img]${href}[/img]\n[i]${label}[/i]` : `[img]${href}[/img]`;
  });

  // Links [text](url)
  text = text.replace(/\[([^\]]+)]\(([^)]+)\)/g, (_m, label, url) => {
    const href = rewriteHref(url.trim());
    return `[url=${href}]${inlineMarkdown(label)}[/url]`;
  });

  // Headings
  text = text.replace(/^######\s+(.+)$/gm, '[b]$1[/b]');
  text = text.replace(/^#####\s+(.+)$/gm, '[b]$1[/b]');
  text = text.replace(/^####\s+(.+)$/gm, '[b]$1[/b]');
  text = text.replace(/^###\s+(.+)$/gm, '[b][font_size=18]$1[/font_size][/b]');
  text = text.replace(/^##\s+(.+)$/gm, '[b][font_size=20]$1[/font_size][/b]');
  text = text.replace(/^#\s+(.+)$/gm, '[b][font_size=22]$1[/font_size][/b]');

  // Horizontal rules
  text = text.replace(/^(-{3,}|\*{3,}|_{3,})\s*$/gm, '————————');

  // Unordered lists
  text = text.replace(/^(\s*)[-*+]\s+(.+)$/gm, '$1• $2');

  // Bold / italic (order matters)
  text = text.replace(/\*\*\*([^*]+)\*\*\*/g, '[b][i]$1[/i][/b]');
  text = text.replace(/\*\*([^*]+)\*\*/g, '[b]$1[/b]');
  text = text.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '[i]$1[/i]');
  text = text.replace(/___([^_]+)___/g, '[b][i]$1[/i][/b]');
  text = text.replace(/__([^_]+)__/g, '[b]$1[/b]');
  text = text.replace(/(?<!_)_([^_]+)_(?!_)/g, '[i]$1[/i]');

  // Inline code
  text = text.replace(/`([^`]+)`/g, '[code]$1[/code]');

  return text.trim() + '\n';
}

/**
 * @param {string} text
 */
function inlineMarkdown(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '[b]$1[/b]')
    .replace(/\*([^*]+)\*/g, '[i]$1[/i]')
    .replace(/`([^`]+)`/g, '[code]$1[/code]');
}

/**
 * @param {string} markdown
 * @param {(href: string) => string} rewriteHref
 */
export function rewriteMarkdownMedia(markdown, rewriteHref) {
  return markdown
    .replace(/(!\[[^\]]*]\()([^)]+)(\))/g, (_m, pre, src, post) => {
      const s = src.trim();
      if (/^https?:\/\//i.test(s) || s.startsWith('data:')) return `${pre}${s}${post}`;
      return `${pre}${rewriteHref(s)}${post}`;
    })
    .replace(/(<img[^>]+src=["'])([^"']+)(["'])/gi, (_m, pre, src, post) => {
      if (/^https?:\/\//i.test(src) || src.startsWith('data:')) return `${pre}${src}${post}`;
      return `${pre}${rewriteHref(src)}${post}`;
    });
}

/**
 * @param {object} item
 */
export function escapeXml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * @param {Array<{title:string,description:string,link:string,guid:string,date:string,cover:string}>} items
 */
export function buildRss(items) {
  const channelLink = `${CDN_BASE}/${ARTICLES_PREFIX}/rss.xml`;
  const lastBuild = new Date().toUTCString();
  const entries = items
    .map((item) => {
      const pubDate = new Date(`${item.date}T12:00:00Z`).toUTCString();
      const enclosure = item.cover
        ? `\n      <enclosure url="${escapeXml(item.cover)}" type="image/jpeg" />`
        : '';
      return `    <item>
      <title>${escapeXml(item.title)}</title>
      <link>${escapeXml(item.link)}</link>
      <guid isPermaLink="true">${escapeXml(item.guid)}</guid>
      <pubDate>${pubDate}</pubDate>
      <description>${escapeXml(item.description)}</description>${enclosure}
    </item>`;
    })
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Blazium Engine Articles</title>
    <link>${escapeXml(channelLink)}</link>
    <description>Official Blazium Game Engine articles and release notes.</description>
    <language>en-us</language>
    <lastBuildDate>${lastBuild}</lastBuildDate>
${entries}
  </channel>
</rss>
`;
}
