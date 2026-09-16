"""
config.py
---------
Central configuration for the Edge/Contour-Based Object Counter & Sorter.

Keeping all tunable parameters in one place satisfies the
'maintainability' and 'configurability' non-functional requirements:
a user can retune the pipeline for a new dataset without touching
any processing logic.
"""

from dataclasses import dataclass


@dataclass
class PipelineConfig:
    # ---- Pre-processing ----
    blur_kernel: tuple = (5, 5)          # Gaussian blur kernel size
    blur_sigma: float = 0.0              # 0 -> auto-computed by OpenCV
    apply_hist_equalization: bool = True # CLAHE histogram equalization toggle

    # ---- Edge detection (Canny) ----
    canny_low: int = 50
    canny_high: int = 150
    canny_aperture: int = 3

    # ---- Morphology (cleans up broken edges before contouring) ----
    morph_kernel_size: tuple = (3, 3)
    morph_close_iterations: int = 2
    morph_dilate_iterations: int = 1

    # ---- Contour filtering ----
    min_contour_area: float = 150.0      # discard tiny noise contours
    max_contour_area: float = 1_000_000.0

    # ---- Shape classification thresholds ----
    # circularity = 4*pi*Area / Perimeter^2 -> 1.0 is a perfect circle
    circularity_circle_min: float = 0.75
    # aspect ratio (w/h of bounding box) close to 1 -> square-ish
    square_aspect_low: float = 0.85
    square_aspect_high: float = 1.15
    # number of polygon-approximation vertices
    triangle_vertices: int = 3
    square_rect_vertices: tuple = (4,)

    # ---- Size buckets (in pixels^2, relative to detected contour area) ----
    small_max_area: float = 1500.0
    medium_max_area: float = 6000.0
    # anything larger than medium_max_area is classified as "large"

    # ---- Output ----
    output_dir: str = "output"
    annotated_image_name: str = "annotated_result.png"
    report_csv_name: str = "detection_report.csv"
    log_file_name: str = "pipeline.log"


DEFAULT_CONFIG = PipelineConfig()
