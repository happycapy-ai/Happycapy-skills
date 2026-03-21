import { useQuery } from '@tanstack/react-query';
import type { CortexData } from './types';

async function fetchCortexData(): Promise<CortexData> {
  const res = await fetch('/api/data');
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function useCortexData() {
  return useQuery({
    queryKey: ['cortex-data'],
    queryFn: fetchCortexData,
    refetchInterval: 5000,
    staleTime: 3000,
  });
}
