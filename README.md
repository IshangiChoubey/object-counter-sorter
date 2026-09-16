# Edge/Contour-Based Object Counter & Sorter

A classical Computer Vision pipeline that detects, counts, and sorts objects
(coins, shapes, or similar items) in an image using **Canny edge detection**,
**contour analysis**, and **geometric shape/size classification** — built as
the course project for **CSE3010 – Computer Vision**.

No machine learning / training data is required: every decision is made
from geometric descriptors (area, perimeter, circularity, polygon vertex
count), making the system fast, deterministic, and easy to explain.

---

## Overview

Given a single input image, the system:

1. **Pre-processes** the image (grayscale conversion, CLAHE histogram
   equalization, Gaussian blur).
2. **Detects edges and segments objects** using Canny edge detection,
   morphological clean-up, and contour extraction.
3. **Classifies and reports** each detected object by shape
   (circle / triangle / square / rectangle / polygon) and size
   (small / medium / large), then produces an annotated image and a CSV
   report.

## Features

- Three independent functional modules: **Pre-processing**,
  **Detection & Segmentation**, **Classification & Reporting**.
- Fully configurable via `modules/config.py` (thresholds for Canny,
  contour area, circularity, size buckets).
- Command-line interface with argument overrides (`--min-area`,
  `--canny-low`, `--canny-high`).
- Annotated output image with per-object bounding boxes, contour outline,
  shape/size label, and centroid marker.
- CSV report with full geometric descriptors per object.
- Console + file logging of every pipeline run (`output/pipeline.log`).
- Input validation with clear, actionable error messages.
- 25 automated unit tests covering every module.
- Two ready-to-run synthetic sample images (mixed geometric shapes, and
  simulated coins) so the project can be demonstrated with **zero external
  dataset downloads**.

## Technologies / Tools Used

| Component        | Technology            |
|-------------------|-----------------------|
| Language          | Python 3.10+           |
| Computer Vision   | OpenCV (`opencv-python-headless`) |
| Numerical ops     | NumPy                  |
| Visualization (report figures) | Matplotlib |
| Testing           | `unittest` (standard library) |
| Version control   | Git / GitHub           |

## Project Structure

```
object-counter-sorter/
├── main.py                        # CLI entry point — orchestrates the pipeline
├── generate_sample_images.py      # Creates synthetic demo images
├── make_diagrams.py                # Generates report design-diagram images
├── make_stage_figure.py            # Generates the pipeline-stages figure
├── requirements.txt
├── README.md
├── statement.md
├── modules/
│   ├── __init__.py
│   ├── config.py                  # All tunable parameters (PipelineConfig)
│   ├── logger_utils.py            # Shared logging setup
│   ├── validation.py              # Input validation & custom exceptions
│   ├── preprocessing.py           # Functional Module 1
│   ├── edge_detection.py          # Functional Module 2 (edges)
│   ├── segmentation.py            # Functional Module 2 (contours)
│   ├── shape_classifier.py        # Functional Module 3 (classification)
│   ├── annotator.py               # Draws results on the image
│   └── reporting.py               # CSV + summary statistics
├── tests/
│   ├── test_preprocessing.py
│   ├── test_edge_detection.py
│   ├── test_segmentation.py
│   ├── test_shape_classifier.py
│   └── test_validation_and_reporting.py
├── sample_images/
│   ├── shapes_sample.png
│   └── coins_sample.png
├── output/                        # Created automatically at run time
│   ├── annotated_result.png
│   ├── edge_map.png
│   ├── detection_report.csv
│   └── pipeline.log
└── docs/
    └── diagrams/                  # Architecture / UML diagrams used in the report
```

## Steps to Install & Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/object-counter-sorter.git
cd object-counter-sorter
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the sample images (first run only)
```bash
python generate_sample_images.py
```

### 5. Run the pipeline
```bash
# Mixed geometric shapes
python main.py --image sample_images/shapes_sample.png --output output/shapes_run

# Coin-like objects
python main.py --image sample_images/coins_sample.png --output output/coins_run --min-area 300
```

### 6. Use your own image
```bash
python main.py --image path/to/your_image.png --output output/my_run
```

Optional overrides:
```bash
python main.py --image sample_images/coins_sample.png \
                --output output/tuned_run \
                --min-area 400 \
                --canny-low 40 \
                --canny-high 130
```

## Output

After a run, the specified `--output` folder contains:

| File | Description |
|---|---|
| `annotated_result.png` | Original image with contours, bounding boxes, IDs, and shape/size labels drawn |
| `edge_map.png` | The cleaned Canny edge map used for contour extraction |
| `detection_report.csv` | One row per detected object with all geometric descriptors |
| `pipeline.log` | Full run log (INFO/DEBUG/ERROR) |

The console additionally prints a summary such as:
```
===== DETECTION SUMMARY =====
Total objects detected : 13
By shape:
  circle    : 13
By size:
  medium    : 8
  large     : 5
==============================
```

## Instructions for Testing

Run the full automated test suite (25 unit tests across every module):
```bash
python -m unittest discover -s tests -v
```

All tests are deterministic (they use synthetic in-memory images), so no
external files or network access are required.

## Screenshots

See `docs/diagrams/pipeline_stages.png` for a side-by-side view of every
pre-processing stage, and the project report (submitted separately as PDF)
for full annotated-output screenshots on both sample images.

## Configuration

All thresholds live in `modules/config.py` as a single `PipelineConfig`
dataclass, so retuning the system for a new type of image (different
lighting, object size, background) requires editing values in one place —
no changes to processing logic are needed.

## License

This project was built for academic purposes as part of the CSE3010
Computer Vision course (VITyarthi "Build Your Own Project" evaluation).
