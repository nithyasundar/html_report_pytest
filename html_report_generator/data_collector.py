"""
Collect and normalize test result data into a simplified structure used by the renderer.
This module is intentionally tolerant of different input types: dicts produced by other
tools or pytest terminal/report objects.
"""
from typing import Any, Dict, Iterable, List
import time


def _as_dict(item: Any) -> Dict:
    """
    Try to normalize a single test result item into a dict with expected keys.
    Expected keys:
        - nodeid (str)
        - outcome (str)  # 'passed', 'failed', 'skipped'
        - duration (float)  # seconds
        - longrepr (str) optional
        - when (str) optional  # 'call', 'setup', 'teardown'
    """
    if isinstance(item, dict):
        return dict(item)
    # Best-effort mapping for common pytest objects
    result = {}
    for k in ("nodeid", "outcome", "duration", "longrepr", "when"):
        try:
            result[k] = getattr(item, k)
        except Exception:
            result[k] = None
    # fallback: use str() and sensible defaults
    result.setdefault("nodeid", getattr(item, "nodeid", str(item)))
    result.setdefault("outcome", getattr(item, "outcome", "unknown"))
    result.setdefault("duration", getattr(item, "duration", 0.0) or 0.0)
    result.setdefault("longrepr", getattr(item, "longrepr", ""))
    result.setdefault("when", getattr(item, "when", "call"))
    return result


def collect_report_data(items: Iterable[Any]) -> Dict[str, Any]:
    """
    Accept an iterable of result items and produce a normalized summary dict.
    Summary keys:
      - generated_at (float epoch)
      - counts: {passed, failed, skipped, total}
      - duration_total (float)
      - tests: list of normalized test dicts
    """
    start = time.time()
    tests: List[Dict[str, Any]] = []
    counts = {"passed": 0, "failed": 0, "skipped": 0, "unknown": 0}
    total_duration = 0.0

    for it in items:
        d = _as_dict(it)
        outcome = (d.get("outcome") or "unknown").lower()
        if outcome not in counts:
            outcome = "unknown"
        counts[outcome] += 1
        try:
            duration = float(d.get("duration") or 0.0)
        except Exception:
            duration = 0.0
        total_duration += duration
        tests.append(
            {
                "nodeid": d.get("nodeid", ""),
                "outcome": outcome,
                "duration": duration,
                "longrepr": d.get("longrepr") or "",
                "when": d.get("when", "call"),
            }
        )

    summary = {
        "generated_at": start,
        "counts": {**counts, "total": sum(counts.values())},
        "duration_total": total_duration,
        "tests": tests,
    }
    return summary