# LLM Prompt Templates

## Article Rewrite Prompt

You are an expert news editor and SEO specialist. Your job is to rewrite news articles
to be more engaging, SEO-friendly, and accurate while maintaining the core facts.

Article Title: {title}
Article Content: {content}

Please rewrite this article with the following requirements:
1. Make it 30% more engaging and readable
2. Add a compelling introduction (2-3 sentences)
3. Optimize for SEO (natural keywords, good structure)
4. Keep all factual accuracy
5. Add subheadings to break up content
6. Include a brief conclusion

Return the rewritten article in JSON format:
{
  "title": "New title (max 70 chars)",
  "subtitle": "Subtitle for article",
  "content": "Full rewritten article",
  "summary": "2-3 sentence summary",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}

## SEO Meta Generation Prompt

Generate SEO metadata for this news article.

Title: {title}
Content: {content}

Provide JSON with:
- meta_description: Max 160 characters, compelling description
- keywords: List of 5-10 relevant keywords
- og_title: OpenGraph title (max 55 chars)
- og_description: OpenGraph description (max 155 chars)
- canonical_url: Full canonical URL

Return as JSON.

## Fact-Checking Prompt

Verify the following claim from a news article:

Claim: {claim}
Article Title: {title}

Provide:
1. Is this claim likely true? (yes/no/unknown)
2. Confidence level (0-100%)
3. Why you think so
4. Suggested fact-check sources

Return as JSON.
