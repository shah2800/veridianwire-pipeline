'use client';

import { useState } from 'react';
import Image from 'next/image';
import { cn, getArticleCategory } from '@/lib/utils';
import type { PublishedArticle } from '@/types/article';
import { resolveArticleMedia, getPlaceholderPath } from '@/lib/media';

interface ArticleImageProps {
  article: PublishedArticle;
  alt: string;
  className?: string;
  fill?: boolean;
  priority?: boolean;
  sizes?: string;
}

export function ArticleImage({
  article,
  alt,
  className,
  fill = true,
  priority,
  sizes = '100vw',
}: ArticleImageProps) {
  const media = resolveArticleMedia(article);
  const [src, setSrc] = useState(media.imageUrl);
  const [failed, setFailed] = useState(false);
  const category = getArticleCategory(article);
  const fallback = getPlaceholderPath(category);
  const isLocal = src.startsWith('/');

  const handleError = () => {
    if (!failed) {
      setFailed(true);
      setSrc(fallback);
    }
  };

  if (failed || (media.isPlaceholder && isLocal)) {
    return (
      <Image
        src={fallback}
        alt={alt}
        fill={fill}
        unoptimized
        className={cn('object-cover', className)}
        sizes={sizes}
        priority={priority}
      />
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      fill={fill}
      className={cn('object-cover', className)}
      sizes={sizes}
      priority={priority}
      onError={handleError}
    />
  );
}
