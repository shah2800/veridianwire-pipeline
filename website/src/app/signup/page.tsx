'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { createClient } from '@/lib/supabase-browser';
import { signupSchema } from '@/lib/auth-schemas';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { SITE } from '@/lib/site';

export default function SignupPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    const result = signupSchema.safeParse({ fullName, email, password, confirmPassword });
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
      const { data, error } = await supabase.auth.signUp({
        email: result.data.email,
        password: result.data.password,
        options: {
          data: { full_name: result.data.fullName },
        },
      });

      if (error) {
        toast.error(error.message);
        return;
      }

      if (data.user) {
        await supabase.from('profiles').upsert({
          id: data.user.id,
          email: result.data.email,
          full_name: result.data.fullName,
          role: 'user',
          updated_at: new Date().toISOString(),
        });
      }

      toast.success('Account created! Check your email to verify.');
      router.push('/dashboard');
      router.refresh();
    } catch {
      toast.error('Sign up failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-12">
      <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-8 text-center">
          <Link href="/" className="inline-flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-news-red">
              <span className="font-serif text-lg font-bold text-white">AN</span>
            </div>
          </Link>
          <h1 className="mt-4 font-serif text-2xl font-bold text-slate-900">Create account</h1>
          <p className="mt-1 text-sm text-slate-600">Join {SITE.name} for personalized updates</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            id="fullName"
            label="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            error={errors.fullName}
            placeholder="Jane Doe"
            autoComplete="name"
          />
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
            placeholder="Min 8 chars, 1 uppercase, 1 number"
            autoComplete="new-password"
          />
          <Input
            id="confirmPassword"
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            error={errors.confirmPassword}
            placeholder="••••••••"
            autoComplete="new-password"
          />
          <Button type="submit" loading={loading} className="w-full" size="lg">
            Create Account
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-600">
          Already have an account?{' '}
          <Link href="/login" className="font-semibold text-news-red hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
