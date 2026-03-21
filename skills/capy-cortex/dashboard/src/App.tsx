import { useCortexData } from './lib/api';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import MetricsGrid from './components/metrics/MetricsGrid';
import HealthGauge from './components/charts/HealthGauge';
import CategoryDonut from './components/charts/CategoryDonut';
import ConfidenceBar from './components/charts/ConfidenceBar';
import EventsTimeline from './components/charts/EventsTimeline';
import SeverityBreakdown from './components/charts/SeverityBreakdown';
import PrinciplesPanel from './components/tables/PrinciplesPanel';
import EventsFeed from './components/tables/EventsFeed';
import AntiPatternsPanel from './components/tables/AntiPatternsPanel';
import RulesPanel from './components/tables/RulesPanel';
import DiaryPanel from './components/tables/DiaryPanel';
import PreferencesPanel from './components/tables/PreferencesPanel';

function LoadingSkeleton() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-50 bg-cortex-card/80 backdrop-blur-xl border-b border-cortex-border">
        <div className="max-w-[1600px] mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="skeleton w-6 h-6 rounded" />
            <div className="skeleton w-40 h-5 rounded" />
          </div>
          <div className="flex items-center gap-4">
            <div className="skeleton w-11 h-11 rounded-full" />
            <div className="skeleton w-24 h-5 rounded-full" />
            <div className="skeleton w-16 h-4 rounded" />
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-[1600px] w-full mx-auto px-6 py-6 space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="skeleton h-24 rounded-xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton h-64 rounded-xl" />
          ))}
        </div>
        <div className="skeleton h-64 rounded-xl" />
      </main>
    </div>
  );
}

export default function App() {
  const { data, isLoading, error, refetch } = useCortexData();

  if (isLoading && !data) {
    return <LoadingSkeleton />;
  }

  if (error && !data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-cortex-terra mb-2">Failed to connect to Cortex API</p>
          <p className="text-sm text-gray-500 mb-4">Make sure dashboard.py is running on port 8787</p>
          <button
            onClick={() => refetch()}
            className="px-4 py-2 bg-cortex-coral/10 text-cortex-coral rounded-lg hover:bg-cortex-coral/20 transition-colors text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header summary={data?.summary} isLoading={isLoading} onRefresh={() => refetch()} />

      <main className="flex-1 max-w-[1600px] w-full mx-auto px-6 py-6 space-y-6">
        {/* Metric Cards */}
        <MetricsGrid summary={data?.summary} />

        {/* Charts Row 1: Health + Category + Confidence */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <HealthGauge score={data?.summary?.health_score ?? 0} />
          <CategoryDonut data={data?.rules_by_category ?? {}} />
          <ConfidenceBar data={data?.confidence_dist ?? {}} />
          <SeverityBreakdown data={data?.ap_by_severity ?? {}} />
        </div>

        {/* Charts Row 2: Timeline (full width) */}
        {data?.events_timeline && data.events_timeline.length > 0 && (
          <EventsTimeline data={data.events_timeline} />
        )}

        {/* Data Panels Row 1 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <PrinciplesPanel principles={data?.top_principles ?? []} />
          <EventsFeed events={data?.recent_events ?? []} />
          <AntiPatternsPanel patterns={data?.anti_patterns_list ?? []} />
        </div>

        {/* Data Panels Row 2 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <RulesPanel rules={data?.recent_rules ?? []} />
          <DiaryPanel entries={data?.recent_diary ?? []} />
          <PreferencesPanel preferences={data?.preferences_list ?? []} />
        </div>
      </main>

      <Footer
        dbSize={data?.summary?.db_size_kb}
        tfidfDirty={data?.summary?.tfidf_dirty}
        diaryCount={data?.summary?.diary_entries}
      />
    </div>
  );
}
