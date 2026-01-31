import { ReactNode } from 'react';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  subtitle?: string;
  action?: ReactNode;
}

export default function EmptyState({ icon, title, subtitle, action }: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      {icon ? (
        <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-white/10">
          {icon}
        </div>
      ) : (
        <svg className="mx-auto h-12 w-12 text-[#a1a1aa]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 002 2h2a2 2 0 002-2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      )}
      <h3 className="mt-2 text-sm font-medium text-white">{title}</h3>
      {subtitle && <p className="mt-1 text-sm text-[#a1a1aa]">{subtitle}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}