import { motion } from 'framer-motion';
import { useAnimatedValue } from '../../hooks/useAnimatedValue';
import type { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: number;
  icon: LucideIcon;
  color: string;
  delay?: number;
}

export default function MetricCard({ label, value, icon: Icon, color, delay = 0 }: MetricCardProps) {
  const animated = useAnimatedValue(value);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="relative overflow-hidden rounded-xl bg-cortex-card border border-cortex-border p-5 hover:border-cortex-border-hover transition-colors group"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500 mb-1">{label}</p>
          <p className="text-3xl font-bold tracking-tight">{animated.toLocaleString()}</p>
        </div>
        <div className={`p-2.5 rounded-lg bg-opacity-10`} style={{ backgroundColor: `${color}15` }}>
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
      </div>
      <div
        className="absolute bottom-0 left-0 h-0.5 transition-all duration-500 group-hover:opacity-100 opacity-50"
        style={{ backgroundColor: color, width: '100%' }}
      />
    </motion.div>
  );
}
