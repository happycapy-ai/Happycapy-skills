import { motion } from 'framer-motion';
import { useAnimatedValue } from '../../hooks/useAnimatedValue';

interface HealthGaugeProps {
  score: number;
}

export default function HealthGauge({ score }: HealthGaugeProps) {
  const radius = 70;
  const circumference = Math.PI * radius; // semi-circle
  const dashOffset = circumference - (score / 100) * circumference;
  const color = score >= 80 ? '#7D9B76' : score >= 50 ? '#f59e0b' : '#C67A6B';
  const animatedScore = useAnimatedValue(score, 1200);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6 }}
      className="rounded-xl bg-cortex-card border border-cortex-border p-5 flex flex-col items-center cortex-panel"
    >
      <h3 className="text-sm font-semibold text-gray-400 mb-2">System Health</h3>
      <svg width="180" height="110" viewBox="0 0 180 110">
        <path
          d="M 10 100 A 70 70 0 0 1 170 100"
          fill="none" stroke="#1f2937" strokeWidth="10" strokeLinecap="round"
        />
        <motion.path
          d="M 10 100 A 70 70 0 0 1 170 100"
          fill="none" stroke={color} strokeWidth="10" strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: dashOffset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        />
        <text x="90" y="90" textAnchor="middle" className="fill-white text-3xl font-bold" fontSize="32">
          {animatedScore}
        </text>
        <text x="90" y="106" textAnchor="middle" className="fill-gray-500" fontSize="11">
          Health Score
        </text>
      </svg>
    </motion.div>
  );
}
