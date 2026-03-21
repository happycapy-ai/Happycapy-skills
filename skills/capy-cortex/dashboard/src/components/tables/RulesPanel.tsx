import { motion } from 'framer-motion';
import { BookOpen } from 'lucide-react';

interface RulesPanelProps {
  rules: Array<{ content: string; category: string; confidence: number; occurrences: number; time: string }>;
}

const CAT_COLORS: Record<string, string> = {
  error: '#C67A6B',
  correction: '#7D9B76',
  skills: '#8B5CF6',
  git: '#3B82F6',
  debugging: '#FF6B4A',
};

export default function RulesPanel({ rules }: RulesPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.55 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <BookOpen className="w-4 h-4 text-[#FF6B4A]" />
        Recent Rules
      </h3>
      <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
        {rules.map((r, i) => {
          const color = CAT_COLORS[r.category] || '#6b7280';
          return (
            <div key={i} className="py-1.5 border-b border-[#1f2937] last:border-0">
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded-full"
                  style={{ backgroundColor: `${color}15`, color }}
                >
                  {r.category}
                </span>
                <span className="text-[10px] text-gray-600">{(r.confidence * 100).toFixed(0)}%</span>
              </div>
              <p className="text-xs text-gray-300 leading-relaxed line-clamp-2">{r.content}</p>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
