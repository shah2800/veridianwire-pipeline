import Link from 'next/link';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { Button } from '@/components/ui/Button';
import { Home, Search } from 'lucide-react';

export default function NotFound() {
  return (
    <SiteLayout>
      <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
        <p className="mb-2 text-6xl font-bold text-news-red">404</p>
        <h1 className="mb-2 font-serif text-3xl font-bold text-slate-900">Page Not Found</h1>
        <p className="mb-8 max-w-md text-slate-600">
          The page you&apos;re looking for doesn&apos;t exist or may have been moved.
        </p>
        <div className="flex gap-3">
          <Link href="/">
            <Button>
              <Home className="h-4 w-4" />
              Go Home
            </Button>
          </Link>
          <Link href="/search">
            <Button variant="outline">
              <Search className="h-4 w-4" />
              Search News
            </Button>
          </Link>
        </div>
      </div>
    </SiteLayout>
  );
}
