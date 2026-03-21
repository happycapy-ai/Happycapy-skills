import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

interface EventsTimelineProps {
  data: Array<{ date: string; total: number }>;
}

export default function EventsTimeline({ data }: EventsTimelineProps) {
  const formatted = data.map(d => ({
    ...d,
    label: new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
  }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4">Learning Timeline</h3>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={formatted}>
          <defs>
            <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FF6B4A" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#FF6B4A" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="label" tick={{ fill: '#9ca3af', fontSize: 10 }}
            axisLine={false} tickLine={false}
          />
          <YAxis hide />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '8px',
              fontSize: '12px',
            }}
            itemStyle={{ color: '#f9fafb' }}
          />
          <Area
            type="monotone" dataKey="total" stroke="#FF6B4A" strokeWidth={2}
            fill="url(#colorTotal)" animationDuration={1200}
          />
        </AreaChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
