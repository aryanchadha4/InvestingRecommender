"""Sweep recommendations across amounts and risk levels."""

import itertools
import json
import sys

import httpx

BASE = "http://localhost:8000"

AMOUNTS = [1000, 5000, 10000, 25000, 50000]
RISKS = ["conservative", "balanced", "aggressive"]
SYMS = ["VOO", "QQQM", "IWM", "EFA", "EMB", "AGG"]  # customize


def pretty_allocation(dollars: dict[str, float]) -> list[tuple[str, float]]:
    """Return top-5 allocations by dollars."""
    return sorted(dollars.items(), key=lambda x: x[1], reverse=True)[:5]


def run():
    """Run the recommendation sweep."""
    with httpx.Client(timeout=60.0) as client:
        # Ensure data present (idempotent)
        print("📊 Backfilling prices and computing signals...")
        client.post(f"{BASE}/api/v1/signals/backfill", params=[("symbols", s) for s in SYMS])
        client.post(f"{BASE}/api/v1/signals/compute", params=[("symbols", s) for s in SYMS])
        print("✅ Data ready\n")

        print("=" * 80)
        print("RECOMMENDATION SWEEP")
        print("=" * 80)

        for amt, risk in itertools.product(AMOUNTS, RISKS):
            r = client.get(
                f"{BASE}/api/v1/recommend/",
                params={"risk": risk, "amount": amt, "symbols": SYMS},
            )
            r.raise_for_status()
            data = r.json()

            dollars = data["allocation_dollars"]
            w = data["allocation_weights"]

            ssum = round(sum(w.values()), 6)
            dsum = round(sum(dollars.values()), 2)

            print(f"\nRisk={risk:<12} Amount=${amt:<7}  Weights≈{ssum}  Dollars≈{dsum}")
            for sym, val in pretty_allocation(dollars):
                print(f"  {sym:<5} ${val:,.2f}  (w={w[sym]:.3f})")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("ERROR:", e)
        import traceback

        traceback.print_exc()
        sys.exit(1)

