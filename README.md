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

## Environment Setup

This project requires **Python 3.10 or newer** and no other software (no database,
no GUI toolkit, no external services). Everything runs from the command line.

### 0. Install Python (skip if already installed)

Check first:
```bash
python --version
```
If this errors or shows a version below 3.10:

- **Windows**: download the installer from [python.org/downloads](https://www.python.org/downloads/).
  On the very first install screen, **check the box "Add python.exe to PATH"** before
  clicking Install. If `python` still isn't recognized afterwards, search Windows for
  **"Manage App Execution Aliases"** and turn OFF the "App Installer python.exe/python3.exe"
  entries (these are fake Microsoft Store stubs that shadow a real install), then reopen
  your terminal.
- **macOS**: `brew install python3` (requires [Homebrew](https://brew.sh)), or download
  from python.org.
- **Linux**: `sudo apt install python3 python3-venv python3-pip` (Debian/Ubuntu) or the
  equivalent for your distribution.

Also ensure Git is installed (to clone the repo): [git-scm.com/downloads](https://git-scm.com/downloads).

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/object-counter-sorter.git
cd object-counter-sorter
```

### 2. Create and activate a virtual environment (recommended, not mandatory)
```bash
python -m venv venv
```
Activate it:
```bash
venv\Scripts\activate           # Windows (PowerShell or cmd)
source venv/bin/activate        # macOS / Linux
```
A successful activation shows `(venv)` at the start of your terminal prompt.

> **Windows PowerShell "running scripts is disabled" error?** Run this once, then retry
> activation:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> Type `Y` to confirm when prompted.

### 3. Install dependencies

Always install using `python -m pip` (not a bare `pip` command) — this guarantees the
packages install into the **same** Python environment that will run the project, which
avoids a common mismatch between a global `pip` and a virtual-environment `python`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify OpenCV installed correctly:
```bash
python -c "import cv2; print(cv2.__version__)"
```
This should print a version number (e.g., `4.10.0`) with no error. If you see
`ModuleNotFoundError: No module named 'cv2'` even after installing, it almost always
means `pip` and `python` are pointing at two different Python installations — re-run
the install with `python -m pip install -r requirements.txt` exactly as shown above
rather than a bare `pip install`.

### 4. Configuration (optional)

No configuration file needs to be created to run the project — sensible defaults are
built in (see `modules/config.py`). Advanced users can tune detection thresholds either
by editing `modules/config.py` directly, or per-run via CLI flags (Step 6 below).

### 5. Generate the sample images (first run only)
```bash
python generate_sample_images.py
```
Expected output:
```
Sample images written to 'sample_images/'.
```

### 6. Run the pipeline
```bash
# Mixed geometric shapes
python main.py --image sample_images/shapes_sample.png --output output/shapes_run

# Coin-like objects
python main.py --image sample_images/coins_sample.png --output output/coins_run --min-area 300
```

Each run prints a detection summary to the console and writes an annotated image, an
edge map, a CSV report, and a log file into the `--output` folder (see "Output" section
below).

### 7. Use your own image
```bash
python main.py --image path/to/your_image.png --output output/my_run
```

Optional threshold overrides (useful for real photographs, which usually need
different tuning than the synthetic samples):
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

Expected final lines:
```
Ran 25 tests in 0.0XXs

OK
```

All tests are deterministic (they use synthetic in-memory images), so no
external files or network access are required.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `python: command not found` | Python isn't installed or not on PATH — see Environment Setup, Step 0 |
| `ModuleNotFoundError: No module named 'cv2'` after installing | `pip` and `python` point to different environments — reinstall with `python -m pip install -r requirements.txt` |
| PowerShell: `running scripts is disabled on this system` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, confirm with `Y`, then retry `venv\Scripts\activate` |
| `ERROR: Input file not found` when running `main.py` | Check the `--image` path is correct and relative to your current terminal directory |
| Annotated image shows 0 objects detected | Your image likely needs different thresholds — try `--min-area`, `--canny-low`, `--canny-high` overrides (Step 7) |

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
