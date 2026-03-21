import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { motion } from 'framer-motion';

interface ConfidenceBarProps {
  data: Record<string, number>;
}

const BAR_COLORS = ['#C67A6B', '#f59e0b', '#9B8B7A', '#7BA3A8', '#7D9B76'];

export default function ConfidenceBar({ data }: ConfidenceBarProps) {
  const chartData = Object.entries(data).map(([range, count]) => ({ range, count }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.25 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4">Confidence Spectrum</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={chartData} barCategoryGap="20%">
          <XAxis
            dataKey="range" tick={{ fill: '#9ca3af', fontSize: 11 }}
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
            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
          />
          <Bar dataKey="count" radius={[6, 6, 0, 0]} animationDuration={1000}>
            {chartData.map((_, i) => (
              <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
