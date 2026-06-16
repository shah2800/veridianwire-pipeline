'use client';

import { cn } from '@/lib/utils';
import { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, id, ...props }, ref) => (
    <div className="w-full">
      {label && (
        <label htmlFor={id} className="mb-1.5 block text-sm font-medium text-slate-700">
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={id}
        className={cn(
          'w-full rounded-md border border-slate-300 bg-white px-4 py-2.5 text-slate-900',
          'placeholder:text-slate-400 transition-colors',
          'focus:border-news-red focus:outline-none focus:ring-2 focus:ring-red-100',
          error && 'border-red-500 focus:border-red-500 focus:ring-red-100',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1.5 text-sm text-red-600">{error}</p>}
    </div>
  )
);

Input.displayName = 'Input';
