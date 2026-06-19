import sanitizeHtml from 'sanitize-html';

const ALLOWED_TAGS = [
  'p', 'br', 'strong', 'em', 'b', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'ul', 'ol', 'li', 'blockquote', 'a', 'span', 'div', 'figure', 'figcaption',
  'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'pre', 'code',
];

const SANITIZE_OPTIONS: sanitizeHtml.IOptions = {
  allowedTags: ALLOWED_TAGS,
  allowedAttributes: {
    a: ['href', 'target', 'rel', 'title'],
    img: ['src', 'alt', 'title', 'width', 'height'],
    '*': ['class'],
  },
  allowedSchemes: ['http', 'https', 'mailto'],
};

export function sanitizeArticleContent(html: string): string {
  return sanitizeHtml(html, SANITIZE_OPTIONS);
}

export function contentToPlainText(html: string): string {
  const sanitized = sanitizeArticleContent(html);
  return sanitized.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

export function extractImageFromHtml(html: string): string | undefined {
  if (!html) return undefined;
  const match = html.match(/<img[^>]+src=["']([^"']+)["']/i);
  if (match?.[1]?.startsWith('http')) return match[1];
  return undefined;
}

export function getDefaultArticleImage(category: string): string {
  return `/api/placeholder?category=${encodeURIComponent(category.toLowerCase())}`;
}
