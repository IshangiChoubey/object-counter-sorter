"""
make_stage_figure.py
---------------------
Utility (not part of the pipeline) that runs each pipeline stage on the
coin sample and saves a side-by-side comparison figure, purely for
inclusion as a screenshot in the project report.
"""
import sys, os
sys.path.insert(0, os.path.abspath("."))

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modules.config import DEFAULT_CONFIG
from modules.preprocessing import preprocess_pipeline
from modules.edge_detection import edge_pipeline

pre = preprocess_pipeline("sample_images/coins_sample.png", DEFAULT_CONFIG)
edges = edge_pipeline(pre["blurred"], DEFAULT_CONFIG)

fig, axes = plt.subplots(1, 5, figsize=(20, 4.2))
stages = [
    ("1. Original", cv2.cvtColor(pre["original"], cv2.COLOR_BGR2RGB)),
    ("2. Grayscale", pre["gray"]),
    ("3. CLAHE Equalized", pre["equalized"]),
    ("4. Gaussian Blurred", pre["blurred"]),
    ("5. Canny Edges (cleaned)", edges["cleaned_edges"]),
]
for ax, (title, img) in zip(axes, stages):
    cmap = None if img.ndim == 3 else "gray"
    ax.imshow(img, cmap=cmap)
    ax.set_title(title, fontsize=12)
    ax.axis("off")

plt.tight_layout()
os.makedirs("docs/diagrams", exist_ok=True)
plt.savefig("docs/diagrams/pipeline_stages.png", dpi=150, bbox_inches="tight")
print("Saved docs/diagrams/pipeline_stages.png")
