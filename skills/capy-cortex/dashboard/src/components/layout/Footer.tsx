import { Activity } from 'lucide-react';

interface FooterProps {
  dbSize?: number;
  tfidfDirty?: boolean;
  diaryCount?: number;
}

export default function Footer({ dbSize, tfidfDirty, diaryCount }: FooterProps) {
  return (
    <footer className="border-t border-cortex-border bg-cortex-card/50 backdrop-blur-sm">
      <div className="max-w-[1600px] mx-auto px-6 h-10 flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-1.5">
          <Activity className="w-3 h-3" />
          <span>Capy Cortex v4</span>
        </div>
        <div className="flex items-center gap-4">
          <span>DB: {dbSize ?? '?'}KB</span>
          <span>TF-IDF: {tfidfDirty ? 'Needs retrain' : 'Trained'}</span>
          <span>{diaryCount ?? 0} sessions analyzed</span>
          <span>Auto-refresh: 5s</span>
        </div>
      </div>
    </footer>
  );
}
