import { motion } from 'framer-motion';

interface SeverityBreakdownProps {
  data: Record<string, number>;
}

const SEVERITY_COLORS: Record<string, string> = {
  critical: '#ef4444',
  high: '#C67A6B',
  medium: '#f59e0b',
  low: '#7BA3A8',
};

export default function SeverityBreakdown({ data }: SeverityBreakdownProps) {
  const total = Object.values(data).reduce((a, b) => a + b, 0) || 1;
  const entries = Object.entries(data).sort((a, b) => {
    const order = ['critical', 'high', 'medium', 'low'];
    return order.indexOf(a[0]) - order.indexOf(b[0]);
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.35 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4">Anti-Pattern Severity</h3>
      <div className="space-y-3">
        {entries.map(([severity, count]) => (
          <div key={severity}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs capitalize text-gray-300">{severity}</span>
              <span className="text-xs text-gray-500">{count}</span>
            </div>
            <div className="h-2 bg-cortex-elevated rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ backgroundColor: SEVERITY_COLORS[severity] || '#6b7280' }}
                initial={{ width: 0 }}
                animate={{ width: `${(count / total) * 100}%` }}
                transition={{ duration: 0.8, delay: 0.4 }}
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
