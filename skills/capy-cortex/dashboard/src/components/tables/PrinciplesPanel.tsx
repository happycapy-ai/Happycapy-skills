import { motion } from 'framer-motion';
import { Lightbulb } from 'lucide-react';

interface PrinciplesPanelProps {
  principles: Array<{ content: string; confidence: number; occurrences: number }>;
}

export default function PrinciplesPanel({ principles }: PrinciplesPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <Lightbulb className="w-4 h-4 text-[#8B5CF6]" />
        Top Principles
      </h3>
      <div className="space-y-3 max-h-[340px] overflow-y-auto pr-1">
        {principles.map((p, i) => (
          <div key={i} className="group">
            <p className="text-xs text-gray-300 leading-relaxed mb-1.5 line-clamp-2">{p.content}</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-1.5 bg-[#1f2937] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#8B5CF6] rounded-full transition-all duration-500"
                  style={{ width: `${p.confidence * 100}%` }}
                />
              </div>
              <span className="text-[10px] text-gray-500 w-8 text-right">{(p.confidence * 100).toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
