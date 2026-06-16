'use client';

import { useState } from 'react';
import { z } from 'zod';
import { Mail, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

const emailSchema = z.string().email('Please enter a valid email');

interface NewsletterFormProps {
  variant?: 'inline' | 'card';
}

export function NewsletterForm({ variant = 'card' }: NewsletterFormProps) {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const result = emailSchema.safeParse(email);
    if (!result.success) {
      setError(result.error.issues[0].message);
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: result.data }),
      });
      const data = await res.json();

      if (data.success) {
        toast.success('Subscribed! Check your inbox for confirmation.');
        setEmail('');
      } else {
        toast.error(data.error || 'Subscription failed. Please try again.');
      }
    } catch {
      toast.error('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (variant === 'inline') {
    return (
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Your email"
          className="flex-1 rounded-md border border-slate-600 bg-slate-800 px-4 py-2 text-sm text-white placeholder:text-slate-400 focus:border-news-red focus:outline-none"
          aria-label="Email for newsletter"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-news-red px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 disabled:opacity-50"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Subscribe'}
        </button>
        {error && <p className="absolute mt-12 text-xs text-red-400">{error}</p>}
      </form>
    );
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-news-red/10">
          <Mail className="h-5 w-5 text-news-red" />
        </div>
        <div>
          <h3 className="font-serif text-lg font-bold text-slate-900">Daily Briefing</h3>
          <p className="text-sm text-slate-600">Top stories delivered to your inbox</p>
        </div>
      </div>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          className="w-full rounded-md border border-slate-300 bg-white px-4 py-2.5 text-sm focus:border-news-red focus:outline-none focus:ring-2 focus:ring-red-100"
          aria-label="Email for newsletter"
        />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-slate-900 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-slate-800 disabled:opacity-50"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              Subscribing...
            </span>
          ) : (
            'Subscribe Free'
          )}
        </button>
      </form>
      <p className="mt-3 text-xs text-slate-500">No spam. Unsubscribe anytime.</p>
    </div>
  );
}
