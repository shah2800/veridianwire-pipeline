"""Detect and prevent AI template placeholders in rewritten articles."""
import re
from typing import List, Optional

# Bracket text that is not a markdown link: [something](url)
_BRACKET_PLACEHOLDER = re.compile(r"\[(?!/)([^\]]{2,})\](?!\()")

_SEO_TEMPLATE_MARKERS = (
    "**Meta Description:**",
    "**Header Tags:**",
    "**Keywords:**",
    "**Title:**",
    "**H1:**",
    "**H2:**",
)

_PLACEHOLDER_HINTS = (
    "name",
    "date",
    "value",
    "percentage",
    "percent",
    "location",
    "city",
    "country",
    "amount",
    "number",
    "price",
    "year",
    "company",
    "insert",
    "placeholder",
    "xxx",
    "tbd",
)


def find_bracket_placeholders(text: str) -> List[str]:
    """Return bracket placeholders like [President's Name] found in text."""
    if not text:
        return []
    found = []
    for match in _BRACKET_PLACEHOLDER.finditer(text):
        inner = match.group(1).strip()
        if inner.lower().startswith("http"):
            continue
        found.append(f"[{inner}]")
    return found


def is_seo_template_output(text: str) -> bool:
    """True when the model returned an SEO brief instead of article prose."""
    if not text:
        return False
    return any(marker in text for marker in _SEO_TEMPLATE_MARKERS)


def has_template_placeholders(text: str) -> bool:
    """True when rewrite contains unfilled [placeholder] tokens."""
    placeholders = find_bracket_placeholders(text)
    if not placeholders:
        return False
    for token in placeholders:
        inner = token[1:-1].strip().lower()
        if any(hint in inner for hint in _PLACEHOLDER_HINTS):
            return True
        # Generic template pattern: Title Case words or possessive like President's Name
        if re.search(r"[A-Z]", token) or "'" in token:
            return True
    return bool(placeholders)


def is_bad_rewrite(text: str) -> bool:
    """True when rewrite should be rejected or retried."""
    if not text or len(text.strip()) < 80:
        return True
    return has_template_placeholders(text) or is_seo_template_output(text)


REWRITE_RULES = """You are a professional news editor. Rewrite the source into a publish-ready news article.

Requirements:
1. Return only the article body as HTML with 4-8 paragraphs using <p> tags (no markdown).
2. Keep every fact accurate. Use real names, dates, numbers, and places from the source and title.
3. NEVER use bracket placeholders such as [President's Name], [current date], [percentage], or similar.
4. NEVER output SEO templates, meta descriptions, header tags, keyword lists, or titles — only article paragraphs.
5. If the title names a person or place, use that name in the article.
6. Do not invent facts that are not supported by the source."""


def build_rewrite_prompt(title: str, content: str, *, strict: bool = False) -> str:
    """Build a Groq/OpenAI rewrite prompt with anti-placeholder rules."""
    extra = ""
    if strict:
        extra = (
            "\nYour previous draft was rejected because it contained placeholder brackets "
            "or SEO template text. Use only concrete facts from the source below.\n"
        )
    body = (content or "")[:8000]
    return f"{REWRITE_RULES}{extra}\nTitle: {title}\n\nSource article:\n{body}"


def extract_clean_summary(content: str, max_len: int = 160) -> Optional[str]:
    """Pick the first clean sentence for meta description (no placeholders)."""
    from fetchers.article_content import plain_text

    text = plain_text(content)
    if not text:
        return None
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        sentence = sentence.strip()
        if len(sentence) < 40:
            continue
        if has_template_placeholders(sentence) or is_seo_template_output(sentence):
            continue
        if len(sentence) > max_len:
            return sentence[: max_len - 3].rstrip() + "..."
        return sentence
    if not has_template_placeholders(text) and not is_seo_template_output(text):
        trimmed = text[:max_len].strip()
        if len(text) > max_len:
            trimmed = trimmed[: max_len - 3].rstrip() + "..."
        return trimmed or None
    return None
