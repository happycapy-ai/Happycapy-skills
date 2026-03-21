export interface CortexSummary {
  rules: number;
  principles: number;
  anti_patterns: number;
  preferences: number;
  diary_entries: number;
  events: number;
  db_size_kb: number;
  tfidf_dirty: boolean;
  health_score: number;
}

export interface CortexData {
  summary: CortexSummary;
  rules_by_category: Record<string, number>;
  rules_by_maturity: Record<string, number>;
  confidence_dist: Record<string, number>;
  events_by_type: Record<string, number>;
  ap_by_severity: Record<string, number>;
  events_timeline: Array<{ date: string; total: number; [key: string]: string | number }>;
  recent_events: Array<{ type: string; time: string; meta: string }>;
  top_principles: Array<{ content: string; confidence: number; occurrences: number }>;
  recent_rules: Array<{ content: string; category: string; confidence: number; occurrences: number; time: string }>;
  anti_patterns_list: Array<{ content: string; severity: string; occurrences: number }>;
  preferences_list: Array<{ content: string; occurrences: number }>;
  recent_diary: Array<{ summary: string; time: string }>;
}
