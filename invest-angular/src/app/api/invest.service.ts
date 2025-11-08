import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { RecommendResponse, Risk } from './invest.models';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class InvestService {
  private base = environment.apiBase;

  constructor(private http: HttpClient) {}

  recommend(amount: number, risk: Risk, symbols: string[]): Observable<RecommendResponse> {
    let params = new HttpParams().set('amount', String(amount)).set('risk', risk);
    symbols.filter(Boolean).forEach(sym => params = params.append('symbols', sym));
    return this.http.get<RecommendResponse>(`${this.base}/api/v1/recommend/`, { params });
  }

  backfill(symbols: string[]) {
    let params = new HttpParams();
    symbols.forEach(s => params = params.append('symbols', s));
    return this.http.post(`${this.base}/api/v1/signals/backfill`, null, { params });
  }

  compute(symbols: string[]) {
    let params = new HttpParams();
    symbols.forEach(s => params = params.append('symbols', s));
    return this.http.post(`${this.base}/api/v1/signals/compute`, null, { params });
  }

  buildUniverse(count = 100, lookbackDays = 365 * 3) {
    return this.http.post(`${this.base}/api/v1/universe/build`, null, {
      params: { count, lookback_days: lookbackDays } as any
    });
  }

  listUniverse() {
    return this.http.get<{count: number; symbols: string[]}>(`${this.base}/api/v1/universe/list`);
  }
}

