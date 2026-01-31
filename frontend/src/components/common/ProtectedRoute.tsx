'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        setIsAuthorized(true);
      } else {
        setIsAuthorized(false);
        router.push('/login');
      }
    }
  }, [isAuthenticated, isLoading, router]);

  if (isAuthorized === null || isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-black">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white/30"></div>
      </div>
    );
  }

  if (!isAuthorized) {
    return null; // Redirect happens in useEffect
  }

  return <>{children}</>;
}