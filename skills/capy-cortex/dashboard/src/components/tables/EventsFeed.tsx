import { motion } from 'framer-motion';
import { Zap, AlertTriangle, BookOpen, Settings, Trash2, Play } from 'lucide-react';

interface EventsFeedProps {
  events: Array<{ type: string; time: string; meta: string }>;
}

const EVENT_ICONS: Record<string, { icon: typeof Zap; color: string }> = {
  reflection: { icon: BookOpen, color: '#7D9B76' },
  tool_failure: { icon: AlertTriangle, color: '#C67A6B' },
  session_reflection: { icon: BookOpen, color: '#7BA3A8' },
  session_start: { icon: Play, color: '#FF6B4A' },
  consolidation: { icon: Settings, color: '#8B5CF6' },
  cleanup: { icon: Trash2, color: '#9B8B7A' },
};

function formatEventTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

export default function EventsFeed({ events }: EventsFeedProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.45 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
        <Zap className="w-4 h-4 text-[#3B82F6]" />
        Recent Events
      </h3>
      <div className="space-y-2 max-h-[340px] overflow-y-auto pr-1">
        {events.map((e, i) => {
          const config = EVENT_ICONS[e.type] || { icon: Zap, color: '#6b7280' };
          const Icon = config.icon;
          return (
            <div key={i} className="flex items-start gap-2.5 py-1.5 border-b border-[#1f2937] last:border-0">
              <div className="mt-0.5 p-1 rounded" style={{ backgroundColor: `${config.color}15` }}>
                <Icon className="w-3 h-3" style={{ color: config.color }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-gray-300">{e.type.replace(/_/g, ' ')}</span>
                  <span className="text-[10px] text-gray-600">{formatEventTime(e.time)}</span>
                </div>
                <p className="text-[10px] text-gray-500 truncate mt-0.5">{e.meta.slice(0, 80)}</p>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
