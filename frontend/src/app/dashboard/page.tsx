'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '../../components/common/ProtectedRoute';
import TaskList from '../../components/tasks/TaskList';
import { useAuth } from '../../hooks/useAuth';

export default function DashboardPage() {
  const router = useRouter();

  // ✅ Hook called ONCE at top level
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  // Redirect if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
      // 🔥 clear auth storage explicitly
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('auth_user');

      router.replace('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex flex-col">
        <nav className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="text-xl font-bold text-white">Todo App</div>
          <div className="flex items-center space-x-4">
            <div className="text-[#a1a1aa]">Loading...</div>
            <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-white/30"></div>
          </div>
        </nav>

        <div className="flex justify-center items-center flex-grow">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white/30"></div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-black flex flex-col">
        <nav className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="text-xl font-bold text-white">Todo App</div>

          <div className="flex items-center space-x-4">
            <span className="text-[#a1a1aa]">Welcome, {user?.username}</span>

            {/* ✅ Correct logout usage */}
            <button
              onClick={async () => {
                await logout();
                router.push('/login');
              }}
              className="text-[#a1a1aa] hover:text-white border border-white/20 bg-transparent hover:bg-white/10 transition-colors duration-200 px-4 py-2 rounded-md"
            >
              Logout
            </button>
          </div>
        </nav>

        <main className="flex-grow p-6">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-white mb-8">
              Task Dashboard
            </h1>
            <TaskList userId={user?.id || ''} />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
