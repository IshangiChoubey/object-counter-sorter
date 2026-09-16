"""
shape_classifier.py
--------------------
FUNCTIONAL MODULE 3: Classification / Sorting

Classifies each DetectedObject by:
    (a) SHAPE  - circle / triangle / square-rectangle / polygon,
                 using polygon-approximation vertex count and circularity.
    (b) SIZE   - small / medium / large, using contour area thresholds.

This corresponds to the 'Prediction or classification' functional
requirement category from the VITyarthi brief, applied to non-ML,
purely geometric descriptors (appropriate for the classical CV
techniques taught in Module 3 of the syllabus).
"""

from typing import List

from modules.config import PipelineConfig
from modules.segmentation import DetectedObject
from modules.logger_utils import get_logger

logger = get_logger(__name__)


def classify_shape(obj: DetectedObject, cfg: PipelineConfig) -> str:
    """
    Decide a shape label using vertex count (from polygon approximation)
    and circularity as a tie-breaker/override for round objects.
    """
    if obj.circularity >= cfg.circularity_circle_min and obj.approx_vertices >= 6:
        return "circle"

    if obj.approx_vertices == cfg.triangle_vertices:
        return "triangle"

    if obj.approx_vertices in cfg.square_rect_vertices:
        x, y, w, h = obj.bounding_box
        aspect_ratio = w / float(h) if h != 0 else 0
        if cfg.square_aspect_low <= aspect_ratio <= cfg.square_aspect_high:
            return "square"
        return "rectangle"

    if obj.approx_vertices >= 5:
        return "polygon"

    return "unknown"


def classify_size(obj: DetectedObject, cfg: PipelineConfig) -> str:
    """Bucket an object into small / medium / large based on contour area."""
    if obj.area <= cfg.small_max_area:
        return "small"
    if obj.area <= cfg.medium_max_area:
        return "medium"
    return "large"


def classify_objects(
    objects: List[DetectedObject], cfg: PipelineConfig
) -> List[DetectedObject]:
    """Mutates and returns the list of DetectedObject with shape/size labels filled in."""
    for obj in objects:
        obj.shape_label = classify_shape(obj, cfg)
        obj.size_label = classify_size(obj, cfg)

    logger.info("Classified %d objects by shape and size.", len(objects))
    return objects
