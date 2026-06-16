'use client';

import { useEffect } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface ErrorBoundaryProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorFallback({ error, reset }: ErrorBoundaryProps) {
  useEffect(() => {
    console.error('Page error:', error);
  }, [error]);

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-red-100">
        <AlertTriangle className="h-10 w-10 text-red-600" />
      </div>
      <h2 className="mb-2 text-2xl font-bold text-slate-900">Something went wrong</h2>
      <p className="mb-6 max-w-md text-slate-600">
        We encountered an unexpected error. Please try again or return to the homepage.
      </p>
      <div className="flex gap-3">
        <Button onClick={reset} variant="primary">
          <RefreshCw className="h-4 w-4" />
          Try Again
        </Button>
        <Button variant="outline" onClick={() => (window.location.href = '/')}>
          Go Home
        </Button>
      </div>
    </div>
  );
}
