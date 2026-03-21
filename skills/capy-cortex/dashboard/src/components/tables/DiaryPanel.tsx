import { motion } from 'framer-motion';
import { BookMarked } from 'lucide-react';

interface DiaryPanelProps {
  entries: Array<{ summary: string; time: string }>;
}

export default function DiaryPanel({ entries }: DiaryPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <BookMarked className="w-4 h-4 text-[#7D9B76]" />
        Session Diary
      </h3>
      <div className="space-y-3 max-h-[340px] overflow-y-auto pr-1">
        {entries.map((e, i) => (
          <div key={i} className="py-2 border-b border-[#1f2937] last:border-0">
            <p className="text-xs text-gray-300 leading-relaxed line-clamp-3">{e.summary}</p>
            <p className="text-[10px] text-gray-600 mt-1">
              {new Date(e.time).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
