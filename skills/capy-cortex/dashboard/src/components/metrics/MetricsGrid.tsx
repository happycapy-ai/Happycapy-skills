import { BookOpen, Lightbulb, ShieldAlert, Heart, BookMarked, Zap } from 'lucide-react';
import MetricCard from './MetricCard';
import type { CortexSummary } from '../../lib/types';

interface MetricsGridProps {
  summary: CortexSummary | undefined;
}

export default function MetricsGrid({ summary }: MetricsGridProps) {
  if (!summary) return null;

  const metrics = [
    { label: 'Rules', value: summary.rules, icon: BookOpen, color: '#FF6B4A' },
    { label: 'Principles', value: summary.principles, icon: Lightbulb, color: '#8B5CF6' },
    { label: 'Anti-Patterns', value: summary.anti_patterns, icon: ShieldAlert, color: '#C67A6B' },
    { label: 'Preferences', value: summary.preferences, icon: Heart, color: '#7BA3A8' },
    { label: 'Diary Entries', value: summary.diary_entries, icon: BookMarked, color: '#7D9B76' },
    { label: 'Events', value: summary.events, icon: Zap, color: '#3B82F6' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {metrics.map((m, i) => (
        <MetricCard key={m.label} {...m} delay={i * 0.08} />
      ))}
    </div>
  );
}
