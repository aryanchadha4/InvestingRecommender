export type Risk = 'conservative' | 'balanced' | 'aggressive';

export interface RecommendResponse {
  inputs: { risk: Risk; amount: number; symbols: string[] };
  allocation_weights: Record<string, number>;
  allocation_dollars: Record<string, number>;
  signals: Array<{ symbol: string; momentum: number; sentiment: number; score: number; date?: string }>;
  cov_estimation_days: number;
  notes?: string[];
}

