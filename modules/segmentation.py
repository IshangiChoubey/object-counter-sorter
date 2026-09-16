"""
segmentation.py
----------------
Part of FUNCTIONAL MODULE 2: Detection & Segmentation

Extracts contours from the cleaned edge map, filters out noise by area,
and computes the geometric descriptors (area, perimeter, bounding box,
centroid) needed for classification in shape_classifier.py.

Relates to Module 3 of the syllabus (Image Segmentation: Edge-Based
approaches to segmentation).
"""

import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple

from modules.config import PipelineConfig
from modules.logger_utils import get_logger

logger = get_logger(__name__)


@dataclass
class DetectedObject:
    """Holds all geometric information extracted for a single detected object."""
    object_id: int
    contour: np.ndarray
    area: float
    perimeter: float
    bounding_box: Tuple[int, int, int, int]  # x, y, w, h
    centroid: Tuple[int, int]
    approx_vertices: int
    circularity: float
    shape_label: str = "unclassified"
    size_label: str = "unclassified"


def find_contours(cleaned_edges: np.ndarray) -> List[np.ndarray]:
    """Find external contours from a binary edge map."""
    contours, _ = cv2.findContours(
        cleaned_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    logger.info("Found %d raw contours.", len(contours))
    return list(contours)


def _safe_centroid(contour: np.ndarray, bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Compute centroid via image moments; fall back to bbox centre if degenerate."""
    moments = cv2.moments(contour)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        return cx, cy
    x, y, w, h = bbox
    return x + w // 2, y + h // 2


def build_detected_objects(
    contours: List[np.ndarray], cfg: PipelineConfig
) -> List[DetectedObject]:
    """
    Filter raw contours by area and package the survivors into
    DetectedObject records with all descriptors pre-computed.
    """
    detected: List[DetectedObject] = []
    next_id = 1

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < cfg.min_contour_area or area > cfg.max_contour_area:
            continue  # discard noise / oversized background contours

        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        centroid = _safe_centroid(contour, (x, y, w, h))

        # Polygon approximation for vertex counting (triangle/square/etc.)
        epsilon = 0.03 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        circularity = float(4 * np.pi * area / (perimeter ** 2))

        detected.append(
            DetectedObject(
                object_id=next_id,
                contour=contour,
                area=area,
                perimeter=perimeter,
                bounding_box=(x, y, w, h),
                centroid=centroid,
                approx_vertices=len(approx),
                circularity=circularity,
            )
        )
        next_id += 1

    logger.info(
        "Retained %d/%d contours after area filtering (min=%.1f, max=%.1f).",
        len(detected), len(contours), cfg.min_contour_area, cfg.max_contour_area,
    )
    return detected


def segmentation_pipeline(cleaned_edges: np.ndarray, cfg: PipelineConfig) -> List[DetectedObject]:
    """Full segmentation stage: contour extraction + filtering + descriptor computation."""
    raw_contours = find_contours(cleaned_edges)
    objects = build_detected_objects(raw_contours, cfg)
    return objects
