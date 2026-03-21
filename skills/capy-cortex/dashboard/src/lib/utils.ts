import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toLocaleString();
}

export function formatTime(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  if (diff < 60_000) return 'just now';
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m ago`;
  if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)}h ago`;
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function severityColor(severity: string): string {
  switch (severity) {
    case 'critical': return 'text-red-400 bg-red-400/10';
    case 'high': return 'text-cortex-terra bg-cortex-terra/10';
    case 'medium': return 'text-amber-400 bg-amber-400/10';
    case 'low': return 'text-cortex-teal bg-cortex-teal/10';
    default: return 'text-gray-400 bg-gray-400/10';
  }
}

export function categoryColor(category: string): string {
  const colors: Record<string, string> = {
    error: '#C67A6B',
    correction: '#7D9B76',
    skills: '#8B5CF6',
    git: '#3B82F6',
    debugging: '#FF6B4A',
    general: '#9B8B7A',
    best_practice: '#7BA3A8',
  };
  return colors[category] || '#6b7280';
}
