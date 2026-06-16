import { parseSeoMeta } from '@/lib/utils';
import { getYouTubeEmbedUrl } from '@/lib/media';

interface ArticleVideoProps {
  videoUrl: string;
  title: string;
}

export function ArticleVideo({ videoUrl, title }: ArticleVideoProps) {
  const embedUrl = getYouTubeEmbedUrl(videoUrl);

  if (embedUrl) {
    return (
      <div className="relative mb-8 aspect-video overflow-hidden rounded-xl bg-black shadow-lg">
        <iframe
          src={embedUrl}
          title={title}
          className="absolute inset-0 h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    );
  }

  if (videoUrl.match(/\.(mp4|webm|mov)(\?|$)/i)) {
    return (
      <div className="relative mb-8 aspect-video overflow-hidden rounded-xl bg-black shadow-lg">
        <video
          src={videoUrl}
          controls
          className="h-full w-full"
          preload="metadata"
        >
          <track kind="captions" />
        </video>
      </div>
    );
  }

  return (
    <div className="mb-8 rounded-xl border border-slate-200 bg-slate-50 p-6 text-center">
      <p className="mb-3 text-sm text-slate-600">This story includes video content</p>
      <a
        href={videoUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center rounded-md bg-news-red px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-700"
      >
        Watch Video →
      </a>
    </div>
  );
}

export function ArticleVideoFromMeta({
  seoMeta,
  title,
}: {
  seoMeta: ReturnType<typeof parseSeoMeta> & { video_url?: string };
  title: string;
}) {
  if (!seoMeta.video_url) return null;
  return <ArticleVideo videoUrl={seoMeta.video_url} title={title} />;
}
