"""
reporting.py
------------
Generates the tabular / statistical output of the pipeline:
    - a per-object CSV report (id, shape, size, area, perimeter, centroid)
    - an aggregate summary (counts per shape, counts per size)

This satisfies the 'Reporting or analytics' functional-requirement
example and the 'clear input/output structure' requirement from the
VITyarthi brief.
"""

import csv
import os
from collections import Counter
from typing import List, Dict

from modules.segmentation import DetectedObject
from modules.logger_utils import get_logger

logger = get_logger(__name__)


def write_csv_report(objects: List[DetectedObject], output_path: str) -> None:
    """Write one row per detected object to a CSV file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    fieldnames = [
        "object_id", "shape_label", "size_label",
        "area_px2", "perimeter_px", "centroid_x", "centroid_y",
        "bbox_x", "bbox_y", "bbox_w", "bbox_h", "circularity",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for obj in objects:
            writer.writerow({
                "object_id": obj.object_id,
                "shape_label": obj.shape_label,
                "size_label": obj.size_label,
                "area_px2": round(obj.area, 2),
                "perimeter_px": round(obj.perimeter, 2),
                "centroid_x": obj.centroid[0],
                "centroid_y": obj.centroid[1],
                "bbox_x": obj.bounding_box[0],
                "bbox_y": obj.bounding_box[1],
                "bbox_w": obj.bounding_box[2],
                "bbox_h": obj.bounding_box[3],
                "circularity": round(obj.circularity, 3),
            })

    logger.info("CSV report written to %s (%d rows).", output_path, len(objects))


def build_summary(objects: List[DetectedObject]) -> Dict[str, Dict[str, int]]:
    """Return counts grouped by shape label and by size label."""
    shape_counts = Counter(obj.shape_label for obj in objects)
    size_counts = Counter(obj.size_label for obj in objects)

    summary = {
        "total_objects": len(objects),
        "by_shape": dict(shape_counts),
        "by_size": dict(size_counts),
    }
    logger.info("Summary computed: %s", summary)
    return summary


def print_summary(summary: Dict) -> None:
    """Pretty-print the summary dict to the console."""
    print("\n===== DETECTION SUMMARY =====")
    print(f"Total objects detected : {summary['total_objects']}")
    print("\nBy shape:")
    for shape, count in summary["by_shape"].items():
        print(f"  {shape:<10}: {count}")
    print("\nBy size:")
    for size, count in summary["by_size"].items():
        print(f"  {size:<10}: {count}")
    print("==============================\n")
