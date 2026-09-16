"""
main.py
-------
Command-line entry point for the Edge/Contour-Based Object Counter &
Sorter.

Usage:
    python main.py --image sample_images/shapes_sample.png
    python main.py --image sample_images/coins_sample.png --output output/coins_run

The script wires together the three functional modules:
    1. Pre-processing        (modules.preprocessing)
    2. Detection/Segmentation(modules.edge_detection + modules.segmentation)
    3. Classification/Report (modules.shape_classifier + modules.reporting)
and writes an annotated image + CSV report + summary to the output folder.
"""

import argparse
import os
import sys
import time

import cv2

from modules.config import DEFAULT_CONFIG
from modules.validation import validate_image_path, validate_output_dir, InvalidInputError
from modules.preprocessing import preprocess_pipeline, ImageLoadError
from modules.edge_detection import edge_pipeline
from modules.segmentation import segmentation_pipeline
from modules.shape_classifier import classify_objects
from modules.annotator import annotate_image
from modules.reporting import write_csv_report, build_summary, print_summary
from modules.logger_utils import get_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Edge/Contour-Based Object Counter & Sorter (CSE3010 Computer Vision project)"
    )
    parser.add_argument("--image", required=True, help="Path to the input image.")
    parser.add_argument(
        "--output", default="output",
        help="Directory to write annotated image, CSV report, and logs (default: ./output).",
    )
    parser.add_argument(
        "--min-area", type=float, default=None,
        help="Override minimum contour area used to filter out noise.",
    )
    parser.add_argument(
        "--canny-low", type=int, default=None, help="Override Canny lower threshold."
    )
    parser.add_argument(
        "--canny-high", type=int, default=None, help="Override Canny upper threshold."
    )
    return parser.parse_args()


def run_pipeline(image_path: str, output_dir: str, cfg=DEFAULT_CONFIG) -> dict:
    """
    Execute the complete counting/sorting pipeline on a single image.
    Returns the summary dictionary (also used by the automated tests).
    """
    logger = get_logger(__name__, log_dir=output_dir, log_file=cfg.log_file_name)
    start_time = time.time()

    try:
        validate_image_path(image_path)
        validate_output_dir(output_dir)

        logger.info("=== Pipeline started for '%s' ===", image_path)

        # ---- Functional Module 1: Pre-processing ----
        pre = preprocess_pipeline(image_path, cfg)

        # ---- Functional Module 2: Detection & Segmentation ----
        edges = edge_pipeline(pre["blurred"], cfg)
        objects = segmentation_pipeline(edges["cleaned_edges"], cfg)

        # ---- Functional Module 3: Classification & Reporting ----
        objects = classify_objects(objects, cfg)
        annotated = annotate_image(pre["original"], objects)
        summary = build_summary(objects)

        # ---- Persist outputs ----
        annotated_path = os.path.join(output_dir, cfg.annotated_image_name)
        csv_path = os.path.join(output_dir, cfg.report_csv_name)
        edges_path = os.path.join(output_dir, "edge_map.png")

        cv2.imwrite(annotated_path, annotated)
        cv2.imwrite(edges_path, edges["cleaned_edges"])
        write_csv_report(objects, csv_path)

        elapsed = time.time() - start_time
        logger.info("Pipeline completed in %.3f seconds.", elapsed)

        print_summary(summary)
        print(f"Annotated image : {annotated_path}")
        print(f"Edge map        : {edges_path}")
        print(f"CSV report      : {csv_path}")
        print(f"Elapsed time    : {elapsed:.3f} s")

        return summary

    except (InvalidInputError, ImageLoadError) as exc:
        logger.error("Pipeline aborted due to invalid input: %s", exc)
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001 - top-level safety net for CLI use
        logger.exception("Unexpected error during pipeline execution.")
        print(f"UNEXPECTED ERROR: {exc}", file=sys.stderr)
        sys.exit(2)


def main():
    args = parse_args()
    cfg = DEFAULT_CONFIG

    if args.min_area is not None:
        cfg.min_contour_area = args.min_area
    if args.canny_low is not None:
        cfg.canny_low = args.canny_low
    if args.canny_high is not None:
        cfg.canny_high = args.canny_high

    run_pipeline(args.image, args.output, cfg)


if __name__ == "__main__":
    main()
