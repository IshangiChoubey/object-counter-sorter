"""
edge_detection.py
------------------
Part of FUNCTIONAL MODULE 2: Detection & Segmentation

Implements Canny edge detection and morphological clean-up, corresponding
to Module 3 of the CSE3010 syllabus (Feature Extraction: Edges - Canny;
Image Segmentation: Edge Based approaches).
"""

import cv2
import numpy as np

from modules.config import PipelineConfig
from modules.logger_utils import get_logger

logger = get_logger(__name__)


def detect_edges(blurred_image: np.ndarray, cfg: PipelineConfig) -> np.ndarray:
    """Run the Canny edge detector on a pre-processed (blurred) grayscale image."""
    edges = cv2.Canny(
        blurred_image,
        threshold1=cfg.canny_low,
        threshold2=cfg.canny_high,
        apertureSize=cfg.canny_aperture,
    )
    logger.debug(
        "Canny edge detection complete (low=%d, high=%d).",
        cfg.canny_low, cfg.canny_high,
    )
    return edges


def clean_edges(edge_image: np.ndarray, cfg: PipelineConfig) -> np.ndarray:
    """
    Apply morphological closing + dilation to bridge small gaps in the
    edge map so that object boundaries form closed contours.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, cfg.morph_kernel_size)

    closed = cv2.morphologyEx(
        edge_image, cv2.MORPH_CLOSE, kernel,
        iterations=cfg.morph_close_iterations,
    )
    dilated = cv2.dilate(closed, kernel, iterations=cfg.morph_dilate_iterations)

    logger.debug(
        "Morphological clean-up done (close_iter=%d, dilate_iter=%d).",
        cfg.morph_close_iterations, cfg.morph_dilate_iterations,
    )
    return dilated


def edge_pipeline(blurred_image: np.ndarray, cfg: PipelineConfig) -> dict:
    """Run edge detection followed by morphological clean-up."""
    raw_edges = detect_edges(blurred_image, cfg)
    cleaned_edges = clean_edges(raw_edges, cfg)
    return {"raw_edges": raw_edges, "cleaned_edges": cleaned_edges}
