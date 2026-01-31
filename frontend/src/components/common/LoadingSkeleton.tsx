interface LoadingSkeletonProps {
  type?: 'card' | 'list' | 'avatar' | 'text' | 'button';
  count?: number;
}

export default function LoadingSkeleton({ type = 'card', count = 1 }: LoadingSkeletonProps) {
  const renderSkeleton = () => {
    switch (type) {
      case 'list':
        return (
          <div className="animate-pulse">
            {[...Array(count)].map((_, index) => (
              <div key={index} className="border-b border-white/10 py-4">
                <div className="h-4 bg-white/10 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-white/10 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        );
      case 'card':
        return (
          <div className="animate-pulse">
            {[...Array(count)].map((_, index) => (
              <div key={index} className="bg-black border border-white/10 rounded-lg p-6 mb-4">
                <div className="h-4 bg-white/10 rounded w-1/3 mb-4"></div>
                <div className="h-3 bg-white/10 rounded w-full mb-2"></div>
                <div className="h-3 bg-white/10 rounded w-5/6 mb-2"></div>
                <div className="h-3 bg-white/10 rounded w-4/6"></div>
              </div>
            ))}
          </div>
        );
      case 'avatar':
        return (
          <div className="animate-pulse flex items-center">
            <div className="rounded-full bg-white/10 h-10 w-10"></div>
            <div className="ml-4">
              <div className="h-3 bg-white/10 rounded w-24 mb-2"></div>
              <div className="h-2 bg-white/10 rounded w-16"></div>
            </div>
          </div>
        );
      case 'text':
        return (
          <div className="animate-pulse">
            <div className="h-4 bg-white/10 rounded w-full mb-2"></div>
            <div className="h-4 bg-white/10 rounded w-5/6 mb-2"></div>
            <div className="h-4 bg-white/10 rounded w-4/6"></div>
          </div>
        );
      case 'button':
        return (
          <div className="animate-pulse">
            <div className="h-10 bg-white/10 rounded-md w-24"></div>
          </div>
        );
      default:
        return (
          <div className="animate-pulse">
            <div className="h-4 bg-white/10 rounded w-3/4"></div>
          </div>
        );
    }
  };

  return <>{renderSkeleton()}</>;
}