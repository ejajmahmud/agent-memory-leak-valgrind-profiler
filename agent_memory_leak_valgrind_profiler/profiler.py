"""Lightweight heap differential memory leak profiler."""
import tracemalloc
from typing import Dict, List, Optional, Tuple, Any

class LeakReport:
    def __init__(self, is_leaking: bool, growth_bytes: int, top_offender: Optional[str]):
        self.is_leaking = is_leaking
        self.growth_bytes = growth_bytes
        self.top_offender = top_offender

class MemoryLeakProfiler:
    """Tracks memory differentials between snapshots to identify leaks."""

    def __init__(self, leak_threshold_bytes: int = 1024 * 50):
        self.leak_threshold_bytes = leak_threshold_bytes
        self.snapshot_start: Optional[tracemalloc.Snapshot] = None

    def start(self):
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        self.snapshot_start = tracemalloc.take_snapshot()

    def stop_and_evaluate(self) -> LeakReport:
        if not self.snapshot_start:
            raise ValueError("Profiler was not started")

        snapshot_end = tracemalloc.take_snapshot()
        top_stats = snapshot_end.compare_to(self.snapshot_start, "lineno")

        total_growth = sum(stat.size_diff for stat in top_stats if stat.size_diff > 0)
        is_leaking = total_growth > self.leak_threshold_bytes

        top_offender = None
        if top_stats and top_stats[0].size_diff > 0:
            top_offender = f"{top_stats[0].traceback[0]}: +{top_stats[0].size_diff}B"

        return LeakReport(is_leaking, total_growth, top_offender)
