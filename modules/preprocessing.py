"""
preprocessing.py
-----------------
FUNCTIONAL MODULE 1: Image Pre-processing

Implements the low-level image processing concepts from Module 1 of the
CSE3010 syllabus (Image Enhancement, Restoration, Histogram Processing,
Convolution and Filtering) as a preparatory stage for edge detection.

Responsibilities:
    1. Validate and load the input image.
    2. Convert to grayscale.
    3. Apply CLAHE-based histogram equalization (contrast enhancement).
    4. Apply Gaussian smoothing (noise suppression before Canny).
"""

import os
import cv2
import numpy as np

from modules.config import PipelineConfig
from modules.logger_utils import get_logger

logger = get_logger(__name__)


class ImageLoadError(Exception):
    """Raised when the input image cannot be read or is invalid."""


def load_image(image_path: str) -> np.ndarray:
    """
    Load an image from disk with validation and error handling.

    Raises
    ------
    ImageLoadError
        If the file does not exist or OpenCV fails to decode it.
    """
    if not os.path.isfile(image_path):
        logger.error("Input file not found: %s", image_path)
        raise ImageLoadError(f"Input file not found: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        logger.error("OpenCV could not decode image: %s", image_path)
        raise ImageLoadError(f"Could not decode image (unsupported/corrupt file): {image_path}")

    logger.info("Loaded image '%s' with shape %s", image_path, image.shape)
    return image


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image to single-channel grayscale."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    logger.debug("Converted image to grayscale.")
    return gray


def equalize_histogram(gray_image: np.ndarray) -> np.ndarray:
    """
    Apply Contrast-Limited Adaptive Histogram Equalization (CLAHE).

    CLAHE is preferred over global cv2.equalizeHist because it avoids
    over-amplifying noise in near-uniform backgrounds, which is common
    in object-counting images (e.g. coins on a plain surface).
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray_image)
    logger.debug("Applied CLAHE histogram equalization.")
    return equalized


def denoise_and_smooth(gray_image: np.ndarray, cfg: PipelineConfig) -> np.ndarray:
    """Apply Gaussian blur to suppress high-frequency noise before edge detection."""
    blurred = cv2.GaussianBlur(gray_image, cfg.blur_kernel, cfg.blur_sigma)
    logger.debug("Applied Gaussian blur with kernel=%s", cfg.blur_kernel)
    return blurred


def preprocess_pipeline(image_path: str, cfg: PipelineConfig) -> dict:
    """
    Run the full pre-processing pipeline and return every intermediate
    result so later stages / the report generator can inspect them.

    Returns
    -------
    dict with keys: 'original', 'gray', 'equalized', 'blurred'
    """
    original = load_image(image_path)
    gray = to_grayscale(original)

    equalized = equalize_histogram(gray) if cfg.apply_hist_equalization else gray
    blurred = denoise_and_smooth(equalized, cfg)

    return {
        "original": original,
        "gray": gray,
        "equalized": equalized,
        "blurred": blurred,
    }
