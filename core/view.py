import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class TemporalScaler:
    def __init__(self):

        self.scales = {
            "hour": 3600,
            "day": 86400,
            "month": 2592000
        }

    def get_window_cutoff(self, scale: str):
        """
        Calculates the nanosecond 'cut-off' point. 
        """
        seconds = self.scales.get(scale.lower(), 86400) # Default to 'day'
        cutoff_ns = (time.time_ns()) - (seconds * 1_000_000_000)
        return cutoff_ns

    def filter_by_delta(self, stream: list, window: str):
        """
        The Filter: Only keeps shards that fall within our chosen window.
        """
        threshold = self.get_window_cutoff(window)

        return [node for node in stream if node['timestamp'] > threshold or node.get('shielded', False)]

if __name__ == "__main__":
    scaler = TemporalScaler()
    now = time.time_ns()

    mock_history = [
        {"id": "recent_code_fix", "timestamp": now - (1800 * 1e9), "content": "Fixed Commit 7 syntax."},
        {"id": "old_roadmap", "timestamp": now - (86400 * 10 * 1e9), "content": "Initial Paris Plan."}
    ]

    print(f"--- [Temporal-RAG] Lens Engagement ---")

    hour_view = scaler.filter_by_delta(mock_history, "hour")
    print(f"Hourly Lens: Found {len(hour_view)} relevant updates.")

    month_view = scaler.filter_by_delta(mock_history, "month")
    print(f"Monthly Lens: Found {len(month_view)} strategic markers.")
