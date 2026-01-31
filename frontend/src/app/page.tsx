'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const { isAuthenticated, isLoading, logout, user } = useAuth();
  const router = useRouter();
  

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white flex flex-col font-sans">
      {/* --- NAVBAR: Separate Look --- */}
      <nav className="w-full py-6 px-10 flex justify-between items-center fixed top-0 z-50 bg-black/50 backdrop-blur-md">
        <div className="text-white font-bold tracking-tight">Todo App</div>
        
        <div className="flex items-center space-x-8 text-sm font-medium">
          {isAuthenticated ? (
            <>
              <span className="text-zinc-400">Welcome, {user?.email}</span>
              <button 
                onClick={() => logout()} 
                className="hover:text-zinc-300 transition"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-zinc-400 hover:text-white transition">Sign In</Link>
              <Link href="/signup" className="text-zinc-400 hover:text-white transition">Sign Up</Link>
            </>
          )}
        </div>
      </nav>

      {/* --- HERO: Centered Full Page Look --- */}
      <main className="flex-grow flex flex-col items-center justify-center text-center px-4 pt-20">
        <div className="max-w-4xl">
          <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-6 leading-tight">
            Manage Your Tasks <br />
            <span className="text-zinc-500">Simply & Efficiently</span>
          </h1>
          
          <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
            Stay organized and productive with our intuitive task management app. 
            Create, edit, and track your tasks effortlessly.
          </p>

          <div className="flex flex-row items-center justify-center space-x-6">
            <Link
              href="/signup"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg text-sm font-medium transition-all shadow-lg"
            >
              Get Started Free
            </Link>

            <Link
              href="/login"
              className="bg-transparent border border-indigo-600 text-indigo-400 hover:bg-indigo-900/50 px-8 py-3 rounded-lg text-sm font-medium transition-all"
            >
              Sign In
            </Link>
          </div>
        </div>
      </main>

      {/* Subtle Footer Accent */}
      <div className="w-full h-px bg-gradient-to-r from-transparent via-zinc-800 to-transparent mb-10"></div>
    </div>
  );
}