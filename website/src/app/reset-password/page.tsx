'use client';

import { useState } from 'react';
import Link from 'next/link';
import { toast } from 'sonner';
import { ArrowLeft, Mail } from 'lucide-react';
import { createClient } from '@/lib/supabase-browser';
import { resetPasswordSchema } from '@/lib/auth-schemas';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { getSiteUrl } from '@/lib/utils';

export default function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const result = resetPasswordSchema.safeParse({ email });
    if (!result.success) {
      setError(result.error.issues[0].message);
      return;
    }

    setLoading(true);
    try {
      const supabase = createClient();
      const { error: authError } = await supabase.auth.resetPasswordForEmail(
        result.data.email,
        { redirectTo: `${getSiteUrl()}/settings?tab=password` }
      );

      if (authError) {
        toast.error(authError.message);
        return;
      }

      setSent(true);
      toast.success('Reset link sent! Check your email.');
    } catch {
      toast.error('Failed to send reset email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <Link
          href="/login"
          className="mb-6 inline-flex items-center gap-1 text-sm text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to sign in
        </Link>

        {sent ? (
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100">
              <Mail className="h-8 w-8 text-emerald-600" />
            </div>
            <h1 className="font-serif text-2xl font-bold text-slate-900">Check your email</h1>
            <p className="mt-2 text-slate-600">
              We sent a password reset link to <strong>{email}</strong>
            </p>
            <Button
              variant="outline"
              className="mt-6"
              onClick={() => { setSent(false); setEmail(''); }}
            >
              Try another email
            </Button>
          </div>
        ) : (
          <>
            <h1 className="font-serif text-2xl font-bold text-slate-900">Reset password</h1>
            <p className="mt-1 mb-6 text-sm text-slate-600">
              Enter your email and we&apos;ll send you a reset link.
            </p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                id="email"
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={error}
                placeholder="you@example.com"
                autoComplete="email"
              />
              <Button type="submit" loading={loading} className="w-full" size="lg">
                Send Reset Link
              </Button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
