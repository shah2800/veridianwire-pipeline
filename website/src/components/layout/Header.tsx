'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X, User, LogOut, LayoutDashboard, Settings, Shield } from 'lucide-react';
import { SearchBar } from '@/components/search/SearchBar';
import { useAuth } from '@/components/providers/AuthProvider';
import { CATEGORIES } from '@/lib/categories';
import { SITE } from '@/lib/site';
import { cn } from '@/lib/utils';

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const pathname = usePathname();
  const { user, profile, loading, signOut } = useAuth();

  const isActive = (path: string) =>
    pathname === path || pathname.startsWith(`${path}/`);

  const handleSignOut = async () => {
    await signOut();
    setUserMenuOpen(false);
    window.location.href = '/';
  };

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur-md">
      <div className="border-b border-slate-100 bg-slate-900 py-1.5 text-center text-xs text-slate-300">
        <span className="font-medium text-white">{SITE.name}</span>
        <span className="mx-2">·</span>
        {SITE.banner}
        <span className="mx-2 hidden sm:inline">·</span>
        <Link href="/about" className="hidden text-slate-300 hover:text-white sm:inline">
          {SITE.aboutLink}
        </Link>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between gap-4">
          <Link href="/" className="flex-shrink-0">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-news-red">
                <span className="font-serif text-lg font-bold text-white">{SITE.initials}</span>
              </div>
              <div className="hidden sm:block">
                <span className="font-serif text-xl font-bold text-slate-900">{SITE.namePrimary}</span>
                <span className="font-serif text-xl font-bold text-news-red"> {SITE.nameAccent}</span>
              </div>
            </div>
          </Link>

          <nav className="hidden items-center gap-1 lg:flex" aria-label="Main navigation">
            <Link
              href="/"
              className={cn(
                'rounded-md px-3 py-2 text-sm font-medium transition-colors',
                isActive('/') && pathname === '/'
                  ? 'bg-red-50 text-news-red'
                  : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
              )}
            >
              Home
            </Link>
            <Link
              href="/news"
              className={cn(
                'rounded-md px-3 py-2 text-sm font-medium transition-colors',
                isActive('/news')
                  ? 'bg-red-50 text-news-red'
                  : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
              )}
            >
              All News
            </Link>
            {CATEGORIES.slice(0, 4).map((cat) => (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                className={cn(
                  'rounded-md px-3 py-2 text-sm font-medium transition-colors',
                  isActive(`/category/${cat.slug}`)
                    ? 'bg-red-50 text-news-red'
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                )}
              >
                {cat.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <SearchBar className="hidden w-48 md:block lg:w-56" />

            {!loading && (
              <>
                {user ? (
                  <div className="relative">
                    <button
                      onClick={() => setUserMenuOpen(!userMenuOpen)}
                      className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-sm font-bold text-slate-700 hover:bg-slate-300"
                      aria-label="User menu"
                    >
                      {(profile?.full_name || user.email || 'U').charAt(0).toUpperCase()}
                    </button>
                    {userMenuOpen && (
                      <>
                        <div
                          className="fixed inset-0 z-10"
                          onClick={() => setUserMenuOpen(false)}
                        />
                        <div className="absolute right-0 z-20 mt-2 w-52 rounded-lg border border-slate-200 bg-white py-1 shadow-lg">
                          <div className="border-b border-slate-100 px-4 py-2">
                            <p className="truncate text-sm font-medium text-slate-900">
                              {profile?.full_name || 'User'}
                            </p>
                            <p className="truncate text-xs text-slate-500">{user.email}</p>
                          </div>
                          <Link
                            href="/dashboard"
                            onClick={() => setUserMenuOpen(false)}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                          >
                            <LayoutDashboard className="h-4 w-4" />
                            Dashboard
                          </Link>
                          <Link
                            href="/settings"
                            onClick={() => setUserMenuOpen(false)}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                          >
                            <Settings className="h-4 w-4" />
                            Settings
                          </Link>
                          {profile?.role === 'admin' && (
                            <Link
                              href="/admin"
                              onClick={() => setUserMenuOpen(false)}
                              className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
                            >
                              <Shield className="h-4 w-4" />
                              Admin
                            </Link>
                          )}
                          <button
                            onClick={handleSignOut}
                            className="flex w-full items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                          >
                            <LogOut className="h-4 w-4" />
                            Sign Out
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                ) : (
                  <div className="hidden items-center gap-2 sm:flex">
                    <Link
                      href="/login"
                      className="rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/signup"
                      className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                    >
                      Sign Up
                    </Link>
                  </div>
                )}
              </>
            )}

            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="rounded-md p-2 text-slate-700 hover:bg-slate-100 lg:hidden"
              aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            >
              {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {mobileOpen && (
        <div className="border-t border-slate-200 bg-white lg:hidden">
          <div className="space-y-1 px-4 py-4">
            <SearchBar className="mb-4" />
            <Link
              href="/"
              onClick={() => setMobileOpen(false)}
              className="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Home
            </Link>
            <Link
              href="/news"
              onClick={() => setMobileOpen(false)}
              className="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              All News
            </Link>
            {CATEGORIES.map((cat) => (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                onClick={() => setMobileOpen(false)}
                className="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                {cat.label}
              </Link>
            ))}
            <Link
              href="/search"
              onClick={() => setMobileOpen(false)}
              className="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Search
            </Link>
            {!loading && !user && (
              <div className="mt-4 flex gap-2 border-t border-slate-200 pt-4">
                <Link
                  href="/login"
                  onClick={() => setMobileOpen(false)}
                  className="flex flex-1 items-center justify-center gap-2 rounded-md border border-slate-300 py-2 text-sm font-medium"
                >
                  <User className="h-4 w-4" />
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  onClick={() => setMobileOpen(false)}
                  className="flex flex-1 items-center justify-center rounded-md bg-slate-900 py-2 text-sm font-semibold text-white"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
