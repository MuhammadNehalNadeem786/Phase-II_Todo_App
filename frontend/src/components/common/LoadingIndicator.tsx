interface LoadingIndicatorProps {
  size?: 'small' | 'medium' | 'large';
  label?: string;
}

export default function LoadingIndicator({ size = 'medium', label }: LoadingIndicatorProps) {
  const sizeClasses = {
    small: 'h-4 w-4',
    medium: 'h-8 w-8',
    large: 'h-12 w-12',
  };

  const spinnerClass = `animate-spin rounded-full border-2 border-current border-t-transparent text-white/30 ${sizeClasses[size]}`;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className={spinnerClass} role="status">
        <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
          Loading...
        </span>
      </div>
      {label && <p className="mt-2 text-sm text-[#a1a1aa]">{label}</p>}
    </div>
  );
}