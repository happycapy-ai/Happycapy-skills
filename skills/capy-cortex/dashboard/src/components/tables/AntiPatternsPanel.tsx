import { motion } from 'framer-motion';
import { ShieldAlert } from 'lucide-react';

interface AntiPatternsPanelProps {
  patterns: Array<{ content: string; severity: string; occurrences: number }>;
}

const SEVERITY_STYLES: Record<string, string> = {
  critical: 'bg-red-400/10 text-red-400',
  high: 'bg-[#C67A6B]/10 text-[#C67A6B]',
  medium: 'bg-amber-400/10 text-amber-400',
  low: 'bg-[#7BA3A8]/10 text-[#7BA3A8]',
};

export default function AntiPatternsPanel({ patterns }: AntiPatternsPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <ShieldAlert className="w-4 h-4 text-[#C67A6B]" />
        Anti-Patterns ({patterns.length})
      </h3>
      <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
        {patterns.map((p, i) => (
          <div key={i} className="py-1.5 border-b border-[#1f2937] last:border-0">
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded-full ${SEVERITY_STYLES[p.severity] || 'bg-gray-400/10 text-gray-400'}`}>
                {p.severity}
              </span>
              {p.occurrences > 1 && (
                <span className="text-[10px] text-gray-600">x{p.occurrences}</span>
              )}
            </div>
            <p className="text-xs text-gray-300 leading-relaxed line-clamp-2">{p.content}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
