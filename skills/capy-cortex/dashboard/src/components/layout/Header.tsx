import { RefreshCw, Brain, Database, Cpu } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';
import type { CortexSummary } from '../../lib/types';

interface HeaderProps {
  summary: CortexSummary | undefined;
  isLoading: boolean;
  onRefresh: () => void;
}

export default function Header({ summary, isLoading, onRefresh }: HeaderProps) {
  const health = summary?.health_score ?? 0;
  const circumference = 2 * Math.PI * 18;
  const dashOffset = circumference - (health / 100) * circumference;

  return (
    <header className="sticky top-0 z-50 bg-cortex-card/80 backdrop-blur-xl border-b border-cortex-border">
      <div className="max-w-[1600px] mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Brain className="w-6 h-6 text-cortex-coral" />
            <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-cortex-moss rounded-full animate-cortex-pulse" />
          </div>
          <h1 className="text-lg font-bold tracking-tight">Cortex Observatory</h1>
        </div>

        <div className="flex items-center gap-6">
          {summary && (
            <>
              <div className="flex items-center gap-2">
                <svg width="44" height="44" className="-rotate-90">
                  <circle cx="22" cy="22" r="18" fill="none" stroke="#1f2937" strokeWidth="3" />
                  <circle
                    cx="22" cy="22" r="18" fill="none"
                    stroke={health >= 80 ? '#7D9B76' : health >= 50 ? '#f59e0b' : '#C67A6B'}
                    strokeWidth="3" strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={dashOffset}
                    className="transition-all duration-1000"
                  />
                </svg>
                <span className="text-sm font-semibold">{health}%</span>
              </div>

              <div className="flex items-center gap-2">
                <Cpu className="w-3.5 h-3.5 text-gray-500" />
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                  summary.tfidf_dirty
                    ? 'bg-amber-400/10 text-amber-400'
                    : 'bg-cortex-moss/10 text-cortex-moss'
                }`}>
                  {summary.tfidf_dirty ? 'TF-IDF Dirty' : 'TF-IDF Fresh'}
                </span>
              </div>

              <div className="flex items-center gap-1.5 text-xs text-gray-500">
                <Database className="w-3.5 h-3.5" />
                <span>{summary.db_size_kb}KB</span>
              </div>
            </>
          )}

          <button
            onClick={onRefresh}
            className="p-2 rounded-lg hover:bg-cortex-elevated transition-colors"
            title="Refresh data"
          >
            <RefreshCw className={cn('w-4 h-4 text-gray-400', isLoading && 'animate-spin')} />
          </button>
        </div>
      </div>
    </header>
  );
}
