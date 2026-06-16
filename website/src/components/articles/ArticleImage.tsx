'use client';

import { useState } from 'react';
import Image from 'next/image';
import { cn, getArticleCategory } from '@/lib/utils';
import type { PublishedArticle } from '@/types/article';
import { resolveArticleMedia, getPlaceholderPath } from '@/lib/media';
import { Newspaper } from 'lucide-react';

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
      <div
        className={cn(
          'flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900',
          fill ? 'absolute inset-0' : 'h-full w-full',
          className
        )}
      >
        <Image
          src={fallback}
          alt={alt}
          fill={fill}
          unoptimized
          className={cn('object-cover', className)}
          sizes={sizes}
          priority={priority}
        />
        <div className="absolute inset-0 flex items-center justify-center bg-black/20">
          <Newspaper className="h-12 w-12 text-white/30" />
        </div>
      </div>
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      fill={fill}
      unoptimized={!isLocal}
      className={cn('object-cover', className)}
      sizes={sizes}
      priority={priority}
      onError={handleError}
    />
  );
}
