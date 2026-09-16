# Project Statement

## Problem Statement

Manually counting and sorting objects in an image — coins on a table,
components on a conveyor belt, cells under a microscope, fruits on a
sorting line — is slow, error-prone, and does not scale. Existing deep
learning object-detection solutions are accurate but are heavyweight,
require labeled training data, and are difficult to justify for simple,
well-controlled scenes where objects are visually distinct from a plain
background.

This project builds a **lightweight, classical Computer Vision pipeline**
that automatically detects, counts, and sorts objects in a static image
using edge detection and contour analysis, without needing a trained
model or labeled dataset. It applies core techniques taught in Module 1
(image enhancement/filtering) and Module 3 (edge detection, feature
extraction, segmentation) of the CSE3010 syllabus to a practical,
end-to-end application.

## Scope of the Project

- Accepts a single static image (PNG/JPG/BMP/TIFF) as input.
- Detects object boundaries using Canny edge detection and morphological
  clean-up.
- Extracts and filters contours to isolate individual objects from noise.
- Classifies each object by **shape** (circle, triangle, square,
  rectangle, polygon) and **size** (small, medium, large) using purely
  geometric descriptors (area, perimeter, circularity, polygon vertex
  count) — no ML training required.
- Produces an annotated output image, a CSV report, and console/log
  summary statistics.
- Ships with two synthetic sample images so the system can be
  demonstrated and unit-tested without any external dataset.

**Out of scope:** real-time video processing, deep-learning-based object
detection/classification, overlapping/occluded object separation, and
multi-camera or 3D reconstruction (these are covered by other modules of
the syllabus and are noted under Future Enhancements in the project
report).

## Target Users

- Students and instructors evaluating classical image-segmentation
  techniques.
- Small-scale automation scenarios such as counting coins, tokens,
  packaged items, or lab samples photographed against a plain background.
- Anyone needing a fast, explainable, dependency-light alternative to a
  trained object-detection model for simple counting/sorting tasks.

## High-Level Features

1. **Pre-processing module** — grayscale conversion, CLAHE histogram
   equalization, Gaussian blur.
2. **Detection & segmentation module** — Canny edge detection,
   morphological closing/dilation, contour extraction with area-based
   noise filtering.
3. **Classification & reporting module** — shape and size classification,
   annotated image generation, CSV export, and summary statistics.
4. Fully configurable thresholds (single `PipelineConfig` dataclass).
5. CLI with parameter overrides, structured logging, and input
   validation with clear error messages.
6. 25 automated unit tests covering all modules.
