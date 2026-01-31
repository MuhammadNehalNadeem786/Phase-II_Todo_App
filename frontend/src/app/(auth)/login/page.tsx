'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../../hooks/useAuth';
import { validateEmail } from '../../../lib/utils';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateEmail(email)) {
      setError('Please enter a valid email');
      return;
    }

    if (!password) {
      setError('Password is required');
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      router.push('/dashboard');
      router.refresh();
    } catch {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-black bg-[radial-gradient(ellipse_at_top,_rgba(255,255,255,0.05),_transparent_60%)]">

      <div className="w-full max-w-sm rounded-2xl border border-white/10 bg-black/90 px-8 py-10 shadow-2xl">

        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-lg font-semibold text-white tracking-wide">
            Todo App
          </h1>
        </div>

        {/* Title */}
        <h2 className="text-center text-2xl font-bold text-white mb-8">
          Sign in
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">

          {error && (
            <div className="rounded-md border border-red-500/30 bg-red-500/10 p-3">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          {/* Email */}
          <div>
            <label className="block text-xs text-zinc-400 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-white/15 bg-black px-4 py-3 text-white placeholder-zinc-500 focus:border-white/40 focus:ring-2 focus:ring-white/10 outline-none"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-xs text-zinc-400 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-white/15 bg-black px-4 py-3 text-white placeholder-zinc-500 focus:border-white/40 focus:ring-2 focus:ring-white/10 outline-none"
            />
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="mt-4 w-full rounded-lg bg-white py-3.5 text-sm font-semibold text-black hover:bg-zinc-200 transition disabled:opacity-50"
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        {/* Footer */}
        <div className="mt-8 text-center space-y-3">
          <Link href="/signup" className="text-sm text-zinc-400 hover:text-white">
            Do not have an account? Sign up
          </Link>

          <div>
            <Link href="/" className="text-xs text-zinc-500 hover:text-white">
              ← Back to home
            </Link>
          </div>
        </div>

      </div>
    </div>
  );
}
