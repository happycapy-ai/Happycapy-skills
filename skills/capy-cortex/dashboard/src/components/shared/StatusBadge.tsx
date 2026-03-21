import { cn } from '../../lib/utils';

interface StatusBadgeProps {
  label: string;
  variant?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  className?: string;
}

const variants = {
  success: 'bg-cortex-moss/10 text-cortex-moss',
  warning: 'bg-amber-400/10 text-amber-400',
  error: 'bg-cortex-terra/10 text-cortex-terra',
  info: 'bg-cortex-teal/10 text-cortex-teal',
  neutral: 'bg-gray-400/10 text-gray-400',
};

export default function StatusBadge({ label, variant = 'neutral', className }: StatusBadgeProps) {
  return (
    <span className={cn('text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full', variants[variant], className)}>
      {label}
    </span>
  );
}
