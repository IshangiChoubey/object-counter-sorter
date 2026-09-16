"""
annotator.py
------------
Draws the detection/classification results back onto the original
image: contour outlines, bounding boxes, object IDs and shape labels.
This is the visual output the user sees (clear input/output structure
requirement).
"""

from typing import List, Dict, Tuple

import cv2
import numpy as np

from modules.segmentation import DetectedObject
from modules.logger_utils import get_logger

logger = get_logger(__name__)

# Distinct BGR colour per shape label for quick visual sorting
SHAPE_COLORS: Dict[str, Tuple[int, int, int]] = {
    "circle": (0, 165, 255),      # orange
    "triangle": (0, 255, 0),      # green
    "square": (255, 0, 0),        # blue
    "rectangle": (255, 0, 255),   # magenta
    "polygon": (0, 255, 255),     # yellow
    "unknown": (128, 128, 128),   # gray
}


def annotate_image(
    original_image: np.ndarray, objects: List[DetectedObject]
) -> np.ndarray:
    """Return a copy of the original image annotated with detection results."""
    annotated = original_image.copy()

    for obj in objects:
        color = SHAPE_COLORS.get(obj.shape_label, (255, 255, 255))

        cv2.drawContours(annotated, [obj.contour], -1, color, 2)

        x, y, w, h = obj.bounding_box
        cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 1)

        label = f"#{obj.object_id} {obj.shape_label}/{obj.size_label}"
        text_origin = (x, max(y - 8, 12))
        cv2.putText(
            annotated, label, text_origin,
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA,
        )
        cv2.circle(annotated, obj.centroid, 3, color, -1)

    summary = f"Total objects detected: {len(objects)}"
    cv2.putText(
        annotated, summary, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3, cv2.LINE_AA,
    )
    cv2.putText(
        annotated, summary, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA,
    )

    logger.info("Annotated image generated for %d objects.", len(objects))
    return annotated
