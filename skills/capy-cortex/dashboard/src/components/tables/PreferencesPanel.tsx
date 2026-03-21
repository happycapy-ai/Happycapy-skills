import { motion } from 'framer-motion';
import { Heart } from 'lucide-react';

interface PreferencesPanelProps {
  preferences: Array<{ content: string; occurrences: number }>;
}

export default function PreferencesPanel({ preferences }: PreferencesPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.65 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <Heart className="w-4 h-4 text-[#7BA3A8]" />
        User Preferences
      </h3>
      <div className="space-y-2 max-h-[340px] overflow-y-auto pr-1">
        {preferences.map((p, i) => (
          <div key={i} className="flex items-start gap-2 py-1.5 border-b border-[#1f2937] last:border-0">
            <span className="text-[10px] text-gray-600 mt-0.5 shrink-0">#{i + 1}</span>
            <p className="text-xs text-gray-300 leading-relaxed">{p.content}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
