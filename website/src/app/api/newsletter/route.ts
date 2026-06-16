import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { subscribeNewsletter } from '@/lib/supabase';

const schema = z.object({
  email: z.string().email(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const result = schema.safeParse(body);

    if (!result.success) {
      return NextResponse.json(
        { success: false, error: 'Invalid email address' },
        { status: 400 }
      );
    }

    const { success, error } = await subscribeNewsletter(result.data.email);

    if (!success) {
      return NextResponse.json(
        { success: false, error: error || 'Subscription failed' },
        { status: 500 }
      );
    }

    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}
