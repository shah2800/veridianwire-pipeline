'use client';

import { useState, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';
import { createClient } from '@/lib/supabase-browser';
import { loginSchema } from '@/lib/auth-schemas';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { SITE } from '@/lib/site';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const returnTo = searchParams.get('returnTo') || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.issues.forEach((err) => {
        if (err.path[0]) fieldErrors[err.path[0] as string] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    setLoading(true);
    try {
      const supabase = createClient();
      const { error } = await supabase.auth.signInWithPassword({
        email: result.data.email,
        password: result.data.password,
      });

      if (error) {
        toast.error(error.message);
        return;
      }

      toast.success('Welcome back!');
      router.push(returnTo);
      router.refresh();
    } catch {
      toast.error('Sign in failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <Input
        id="email"
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={errors.email}
        placeholder="you@example.com"
        autoComplete="email"
      />
      <Input
        id="password"
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        placeholder="••••••••"
        autoComplete="current-password"
      />
      <div className="flex justify-end">
        <Link href="/reset-password" className="text-sm text-news-red hover:underline">
          Forgot password?
        </Link>
      </div>
      <Button type="submit" loading={loading} className="w-full" size="lg">
        Sign In
      </Button>
    </form>
  );
}

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-8 text-center">
          <Link href="/" className="inline-flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-news-red">
              <span className="font-serif text-lg font-bold text-white">AN</span>
            </div>
          </Link>
          <h1 className="mt-4 font-serif text-2xl font-bold text-slate-900">Welcome back</h1>
          <p className="mt-1 text-sm text-slate-600">Sign in to your {SITE.name} account</p>
        </div>

        <Suspense fallback={<div className="h-48 animate-pulse rounded bg-slate-100" />}>
          <LoginForm />
        </Suspense>

        <p className="mt-6 text-center text-sm text-slate-600">
          Don&apos;t have an account?{' '}
          <Link href="/signup" className="font-semibold text-news-red hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
