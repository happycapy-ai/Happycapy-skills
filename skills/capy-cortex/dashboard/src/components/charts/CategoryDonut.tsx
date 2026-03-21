import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

interface CategoryDonutProps {
  data: Record<string, number>;
}

const COLORS: Record<string, string> = {
  error: '#C67A6B',
  correction: '#7D9B76',
  skills: '#8B5CF6',
  git: '#3B82F6',
  debugging: '#FF6B4A',
  general: '#9B8B7A',
  best_practice: '#7BA3A8',
};

export default function CategoryDonut({ data }: CategoryDonutProps) {
  const chartData = Object.entries(data).map(([name, value]) => ({ name, value }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.15 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-4">Rules by Category</h3>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={85}
            paddingAngle={2}
            dataKey="value"
            animationBegin={200}
            animationDuration={1000}
          >
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || '#6b7280'} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '8px',
              fontSize: '12px',
            }}
            itemStyle={{ color: '#f9fafb' }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-3 mt-2 justify-center">
        {chartData.map((entry) => (
          <div key={entry.name} className="flex items-center gap-1.5 text-xs text-gray-400">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[entry.name] || '#6b7280' }} />
            <span className="capitalize">{entry.name}</span>
            <span className="text-gray-600">({entry.value})</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
