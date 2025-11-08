import { Component, signal, computed, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InvestService } from './api/invest.service';
import { RecommendResponse, Risk } from './api/invest.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'Investment Recommender';
  amount = signal<number>(10000);
  risk = signal<Risk>('balanced');
  symbolsText = signal<string>('VOO,QQQM,IWM,EFA,EMB,AGG');
  loading = signal<boolean>(false);
  error = signal<string | null>(null);
  data = signal<RecommendResponse | null>(null);
  universeCount = signal<number>(100);
  universeSymbols = signal<string[]>([]);

  symbols = computed(() =>
    this.symbolsText().split(',').map(s => s.trim()).filter(Boolean)
  );

  constructor(private api: InvestService) {}

  recommend() {
    this.loading.set(true);
    this.error.set(null);
    this.data.set(null);
    this.api.recommend(this.amount(), this.risk(), this.symbols())
      .subscribe({
        next: (res) => { this.data.set(res); this.loading.set(false); },
        error: (err) => { this.error.set(err?.message ?? 'Request failed'); this.loading.set(false); }
      });
  }

  // Optional helpers to prep data before first run
  backfill() {
    this.loading.set(true);
    this.api.backfill(this.symbols()).subscribe({
      next: () => { this.loading.set(false); },
      error: (e) => { this.error.set(e?.message ?? 'Backfill failed'); this.loading.set(false); }
    });
  }

  compute() {
    this.loading.set(true);
    this.api.compute(this.symbols()).subscribe({
      next: () => { this.loading.set(false); },
      error: (e) => { this.error.set(e?.message ?? 'Compute failed'); this.loading.set(false); }
    });
  }

  weightEntries() {
    const d = this.data();
    if (!d) return [];
    return Object.entries(d.allocation_weights);
  }

  dollar(sym: string): number {
    return this.data()?.allocation_dollars[sym] ?? 0;
  }

  trackBySym = (_: number, row: [string, number]) => row[0];

  ngOnInit() {
    this.refreshUniverse();
  }

  buildUniverse() {
    this.loading.set(true);
    this.api.buildUniverse(this.universeCount()).subscribe({
      next: () => {
        this.loading.set(false);
        this.refreshUniverse();
      },
      error: (e) => {
        this.error.set(e?.message ?? 'Universe build failed');
        this.loading.set(false);
      }
    });
  }

  refreshUniverse() {
    this.api.listUniverse().subscribe({
      next: (res) => this.universeSymbols.set(res.symbols),
      error: () => {}
    });
  }
}

