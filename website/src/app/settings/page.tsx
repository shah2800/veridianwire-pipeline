'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';
import { User, Lock, Trash2 } from 'lucide-react';
import { createClient } from '@/lib/supabase-browser';
import { useAuth } from '@/components/providers/AuthProvider';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { ConfirmModal } from '@/components/ui/ConfirmModal';
import { profileSchema, updatePasswordSchema } from '@/lib/auth-schemas';
import { cn } from '@/lib/utils';

function SettingsContent() {
  const { user, profile, loading: authLoading, refreshProfile } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [tab, setTab] = useState<'profile' | 'password'>('profile');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [profileLoading, setProfileLoading] = useState(false);
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    if (searchParams.get('tab') === 'password') setTab('password');
  }, [searchParams]);

  useEffect(() => {
    if (profile) {
      setFullName(profile.full_name || '');
      setEmail(profile.email || user?.email || '');
    } else if (user) {
      setEmail(user.email || '');
      setFullName(user.user_metadata?.full_name || '');
    }
  }, [profile, user]);

  useEffect(() => {
    if (!authLoading && !user) router.push('/login');
  }, [authLoading, user, router]);

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    const result = profileSchema.safeParse({ fullName, email });
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.issues.forEach((err) => {
        if (err.path[0]) fieldErrors[err.path[0] as string] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    if (!user) return;
    setProfileLoading(true);

    try {
      const supabase = createClient();
      await supabase.auth.updateUser({
        email: result.data.email,
        data: { full_name: result.data.fullName },
      });

      await supabase.from('profiles').upsert({
        id: user.id,
        email: result.data.email,
        full_name: result.data.fullName,
        updated_at: new Date().toISOString(),
      });

      await refreshProfile();
      toast.success('Profile updated successfully');
    } catch {
      toast.error('Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    const result = updatePasswordSchema.safeParse({
      currentPassword,
      newPassword,
      confirmPassword,
    });
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.issues.forEach((err) => {
        if (err.path[0]) fieldErrors[err.path[0] as string] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    setPasswordLoading(true);
    try {
      const supabase = createClient();
      const { error } = await supabase.auth.updateUser({
        password: result.data.newPassword,
      });

      if (error) {
        toast.error(error.message);
        return;
      }

      toast.success('Password updated successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch {
      toast.error('Failed to update password');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (!user) return;
    setDeleteLoading(true);

    try {
      const supabase = createClient();
      await supabase.from('profiles').delete().eq('id', user.id);
      await supabase.auth.signOut();
      toast.success('Account deleted');
      router.push('/');
    } catch {
      toast.error('Failed to delete account');
    } finally {
      setDeleteLoading(false);
      setDeleteModalOpen(false);
    }
  };

  if (authLoading) {
    return (
      <SiteLayout>
        <div className="mx-auto max-w-2xl px-4 py-16">
          <div className="h-64 animate-pulse rounded-xl bg-slate-100" />
        </div>
      </SiteLayout>
    );
  }

  return (
    <SiteLayout>
      <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 lg:px-8">
        <h1 className="mb-8 font-serif text-3xl font-bold text-slate-900">Account Settings</h1>

        {/* Tabs */}
        <div className="mb-8 flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
          <button
            onClick={() => setTab('profile')}
            className={cn(
              'flex flex-1 items-center justify-center gap-2 rounded-md py-2.5 text-sm font-medium transition-colors',
              tab === 'profile' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            )}
          >
            <User className="h-4 w-4" />
            Profile
          </button>
          <button
            onClick={() => setTab('password')}
            className={cn(
              'flex flex-1 items-center justify-center gap-2 rounded-md py-2.5 text-sm font-medium transition-colors',
              tab === 'password' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            )}
          >
            <Lock className="h-4 w-4" />
            Password
          </button>
        </div>

        {tab === 'profile' ? (
          <form onSubmit={handleProfileSave} className="space-y-5 rounded-xl border border-slate-200 bg-white p-6">
            <Input
              id="fullName"
              label="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              error={errors.fullName}
            />
            <Input
              id="email"
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={errors.email}
            />
            <Button type="submit" loading={profileLoading}>
              Save Changes
            </Button>
          </form>
        ) : (
          <form onSubmit={handlePasswordChange} className="space-y-5 rounded-xl border border-slate-200 bg-white p-6">
            <Input
              id="currentPassword"
              label="Current Password"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              error={errors.currentPassword}
            />
            <Input
              id="newPassword"
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              error={errors.newPassword}
            />
            <Input
              id="confirmPassword"
              label="Confirm New Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              error={errors.confirmPassword}
            />
            <Button type="submit" loading={passwordLoading}>
              Update Password
            </Button>
          </form>
        )}

        {/* Danger zone */}
        <div className="mt-10 rounded-xl border border-red-200 bg-red-50 p-6">
          <h3 className="mb-2 font-bold text-red-900">Danger Zone</h3>
          <p className="mb-4 text-sm text-red-700">
            Permanently delete your account and all associated data. This cannot be undone.
          </p>
          <Button variant="danger" onClick={() => setDeleteModalOpen(true)}>
            <Trash2 className="h-4 w-4" />
            Delete Account
          </Button>
        </div>
      </div>

      <ConfirmModal
        open={deleteModalOpen}
        title="Delete Account"
        message="Are you sure you want to permanently delete your account? All your data will be removed."
        confirmLabel="Delete Account"
        loading={deleteLoading}
        onConfirm={handleDeleteAccount}
        onCancel={() => setDeleteModalOpen(false)}
      />
    </SiteLayout>
  );
}

export default function SettingsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-50" />}>
      <SettingsContent />
    </Suspense>
  );
}
