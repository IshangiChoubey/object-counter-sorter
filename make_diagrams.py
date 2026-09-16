"""
make_diagrams.py
------------------
Generates all design diagrams required by the VITyarthi report format
using matplotlib shapes (no external diagramming dependency needed):
    1. System Architecture Diagram
    2. Process Flow / Workflow Diagram
    3. Use Case Diagram
    4. Class / Component Diagram
    5. Sequence Diagram

Outputs PNGs into docs/diagrams/ for embedding into the report.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

OUT = "docs/diagrams"
os.makedirs(OUT, exist_ok=True)

def box(ax, xy, w, h, text, fc="#DCEBFF", ec="#2C5C9C", fontsize=10.5, weight="normal", pad=0.04):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad},rounding_size=0.05",
        linewidth=1.6, facecolor=fc, edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, weight=weight, wrap=True)
    return (x, y, w, h)


def arrow(ax, start, end, text=None, color="#333333", style="-|>", connectionstyle="arc3,rad=0.0"):
    a = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=16,
                         color=color, linewidth=1.4, connectionstyle=connectionstyle)
    ax.add_patch(a)
    if text:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + 0.15, text, ha="center", fontsize=9, color=color, style="italic")


def new_fig(w=12, h=7):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


# -----------------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM
# -----------------------------------------------------------------------
def system_architecture():
    fig, ax = new_fig(12, 7.5)
    ax.text(6, 7.15, "System Architecture — Edge/Contour-Based Object Counter & Sorter",
            ha="center", fontsize=13, weight="bold")

    b_input = box(ax, (0.4, 5.6), 2.6, 1.0, "Input Image\n(PNG/JPG/BMP)", fc="#FFF3D6", ec="#B8860B")
    b_cli = box(ax, (4.6, 5.6), 2.8, 1.0, "CLI Layer\nmain.py (argparse)", fc="#E6E6FA", ec="#4B0082")
    b_val = box(ax, (8.4, 5.6), 3.2, 1.0, "Validation Layer\nvalidation.py", fc="#E6E6FA", ec="#4B0082")

    b_pre = box(ax, (0.4, 3.9), 3.4, 1.1, "Module 1: Pre-processing\npreprocessing.py\n(Grayscale, CLAHE, Blur)", fc="#DCEBFF", ec="#2C5C9C")
    b_edge = box(ax, (4.3, 3.9), 3.4, 1.1, "Module 2a: Edge Detection\nedge_detection.py\n(Canny + Morphology)", fc="#DCEBFF", ec="#2C5C9C")
    b_seg = box(ax, (8.2, 3.9), 3.4, 1.1, "Module 2b: Segmentation\nsegmentation.py\n(Contours + Descriptors)", fc="#DCEBFF", ec="#2C5C9C")

    b_cls = box(ax, (0.4, 2.2), 3.4, 1.1, "Module 3: Classification\nshape_classifier.py\n(Shape + Size labels)", fc="#DFF5DF", ec="#2E7D32")
    b_ann = box(ax, (4.3, 2.2), 3.4, 1.1, "Annotator\nannotator.py\n(Draws overlays)", fc="#DFF5DF", ec="#2E7D32")
    b_rep = box(ax, (8.2, 2.2), 3.4, 1.1, "Reporting Engine\nreporting.py\n(CSV + Summary stats)", fc="#DFF5DF", ec="#2E7D32")

    b_log = box(ax, (0.4, 0.5), 3.4, 1.1, "Logging Layer\nlogger_utils.py\n(pipeline.log)", fc="#FDE0E0", ec="#B22222")
    b_cfg = box(ax, (4.3, 0.5), 3.4, 1.1, "Configuration\nconfig.py\n(Tunable thresholds)", fc="#FDE0E0", ec="#B22222")
    b_out = box(ax, (8.2, 0.5), 3.4, 1.1, "Output Artifacts\nannotated_result.png\ndetection_report.csv", fc="#FFF3D6", ec="#B8860B")

    # flows
    arrow(ax, (3.0, 6.1), (4.6, 6.1))
    arrow(ax, (7.4, 6.1), (8.4, 6.1))
    arrow(ax, (10.0, 5.6), (10.0, 5.0))
    arrow(ax, (2.1, 5.6), (2.1, 5.0))
    arrow(ax, (3.8, 4.45), (4.3, 4.45))
    arrow(ax, (7.7, 4.45), (8.2, 4.45))
    arrow(ax, (2.1, 3.9), (2.1, 3.3))
    arrow(ax, (9.9, 3.9), (5.95, 3.3), connectionstyle="arc3,rad=-0.15")
    arrow(ax, (3.8, 2.75), (4.3, 2.75))
    arrow(ax, (7.7, 2.75), (8.2, 2.75))
    arrow(ax, (9.9, 2.2), (9.9, 1.6))

    # cross-cutting concerns (config/logging feed every module)
    for bx in [b_pre, b_edge, b_seg, b_cls, b_ann, b_rep]:
        pass
    ax.text(6, 1.85, "↑  Configuration & Logging are cross-cutting concerns used by every module above  ↑",
            ha="center", fontsize=9, style="italic", color="#555555")

    plt.tight_layout()
    plt.savefig(f"{OUT}/system_architecture.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# -----------------------------------------------------------------------
# 2. WORKFLOW / PROCESS FLOW DIAGRAM
# -----------------------------------------------------------------------
def workflow_diagram():
    steps = [
        ("Start: Provide image path via CLI", "#FFF3D6", "#B8860B"),
        ("Validate input path & extension", "#E6E6FA", "#4B0082"),
        ("Load image (OpenCV)", "#DCEBFF", "#2C5C9C"),
        ("Convert to Grayscale", "#DCEBFF", "#2C5C9C"),
        ("CLAHE Histogram Equalization", "#DCEBFF", "#2C5C9C"),
        ("Gaussian Blur (noise removal)", "#DCEBFF", "#2C5C9C"),
        ("Canny Edge Detection", "#DFF5DF", "#2E7D32"),
        ("Morphological Close + Dilate", "#DFF5DF", "#2E7D32"),
        ("Find External Contours", "#DFF5DF", "#2E7D32"),
        ("Filter by Area (remove noise)", "#DFF5DF", "#2E7D32"),
        ("Compute Descriptors (area, perimeter,\nvertices, circularity)", "#DFF5DF", "#2E7D32"),
        ("Classify Shape & Size", "#FDE0E0", "#B22222"),
        ("Annotate Image with Results", "#FDE0E0", "#B22222"),
        ("Write CSV Report + Summary", "#FDE0E0", "#B22222"),
        ("End: Display Summary & Save Outputs", "#FFF3D6", "#B8860B"),
    ]

    step_h = 0.85
    gap = 0.35
    n = len(steps)
    fig_h = n * (step_h + gap) + 1.3
    fig, ax = new_fig(4.6, fig_h)
    ax.text(2.3, fig_h - 0.4, "Process Flow", ha="center", fontsize=14, weight="bold")

    xs = 0.5
    w = 3.6
    y = fig_h - 1.1
    positions = []
    for text, fc, ec in steps:
        box(ax, (xs, y - step_h), w, step_h, text, fc=fc, ec=ec, fontsize=9.2, pad=0.02)
        positions.append((y, y - step_h))
        y -= (step_h + gap)

    for i in range(len(positions) - 1):
        top_of_next = positions[i + 1][0]
        bottom_of_cur = positions[i][1]
        arrow(ax, (2.3, bottom_of_cur), (2.3, top_of_next))

    plt.tight_layout()
    plt.savefig(f"{OUT}/workflow_diagram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# -----------------------------------------------------------------------
# 3. USE CASE DIAGRAM
# -----------------------------------------------------------------------
def use_case_diagram():
    fig, ax = new_fig(10, 7.6)
    ax.text(5, 7.2, "Use Case Diagram", ha="center", fontsize=13, weight="bold")

    # Actor (stick figure) - User
    ax.plot(1.1, 5.3, marker="o", markersize=18, color="#333333")
    ax.plot([1.1, 1.1], [5.05, 4.2], color="#333333", linewidth=2)
    ax.plot([0.75, 1.45], [4.75, 4.75], color="#333333", linewidth=2)
    ax.plot([1.1, 0.75], [4.2, 3.6], color="#333333", linewidth=2)
    ax.plot([1.1, 1.45], [4.2, 3.6], color="#333333", linewidth=2)
    ax.text(1.1, 3.25, "User /\nStudent", ha="center", fontsize=10, weight="bold")

    system_box = FancyBboxPatch((3.0, 0.35), 6.5, 6.25, boxstyle="round,pad=0.3",
                                 facecolor="none", edgecolor="#2C5C9C", linewidth=1.8)
    ax.add_patch(system_box)
    ax.text(6.25, 6.35, "Object Counter & Sorter System", ha="center", fontsize=11, weight="bold", color="#2C5C9C")

    use_cases = [
        "Provide Input Image",
        "Configure Detection\nParameters",
        "Run Detection Pipeline",
        "View Annotated Output",
        "Export CSV Report",
        "View Summary Statistics",
        "Inspect Log File",
    ]
    ys = [5.55, 4.75, 3.95, 3.15, 2.35, 1.55, 0.75]
    for text, cy in zip(use_cases, ys[:len(use_cases)]):
        ell = Ellipse((6.4, cy), 4.6, 0.6, facecolor="#DCEBFF", edgecolor="#2C5C9C", linewidth=1.3)
        ax.add_patch(ell)
        ax.text(6.4, cy, text, ha="center", va="center", fontsize=8.5)
        arrow(ax, (1.5, 4.9), (4.1, cy), color="#666666")

    plt.tight_layout()
    plt.savefig(f"{OUT}/use_case_diagram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# -----------------------------------------------------------------------
# 4. CLASS / COMPONENT DIAGRAM
# -----------------------------------------------------------------------
def class_diagram():
    fig, ax = new_fig(13, 8.5)
    ax.text(6.5, 8.15, "Class / Component Diagram", ha="center", fontsize=13, weight="bold")

    def class_box(xy, w, h, title, attrs, methods, fc="#DCEBFF", ec="#2C5C9C"):
        x, y = xy
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.0",
                                     facecolor=fc, edgecolor=ec, linewidth=1.5))
        ax.plot([x, x + w], [y + h - 0.42, y + h - 0.42], color=ec, linewidth=1.1)
        n_attr_lines = len(attrs)
        attr_block_h = 0.28 * n_attr_lines + 0.1
        ax.plot([x, x + w], [y + h - 0.42 - attr_block_h, y + h - 0.42 - attr_block_h], color=ec, linewidth=1.1)
        ax.text(x + w / 2, y + h - 0.24, title, ha="center", va="center", fontsize=9.5, weight="bold")
        ay = y + h - 0.52
        for a in attrs:
            ax.text(x + 0.12, ay, f"- {a}", ha="left", va="center", fontsize=7.6)
            ay -= 0.28
        ay -= 0.06
        for m in methods:
            ax.text(x + 0.12, ay, f"+ {m}()", ha="left", va="center", fontsize=7.6)
            ay -= 0.26

    class_box((0.3, 5.7), 3.1, 2.4, "PipelineConfig",
               ["blur_kernel", "canny_low/high", "min_contour_area", "circularity thresholds", "size thresholds"],
               [])

    class_box((3.9, 5.7), 3.3, 2.0, "DetectedObject",
               ["object_id", "contour", "area, perimeter", "bounding_box, centroid", "shape_label, size_label"],
               [])

    class_box((7.7, 5.7), 2.6, 1.5, "ImageLoadError /\nInvalidInputError",
               ["message"], [])

    class_box((10.8, 5.7), 2.0, 1.5, "Logger\n(logger_utils)",
               ["name", "handlers"], ["get_logger"])

    class_box((0.3, 3.0), 3.0, 1.9, "preprocessing",
               [], ["load_image", "to_grayscale", "equalize_histogram", "denoise_and_smooth", "preprocess_pipeline"], fc="#DFF5DF", ec="#2E7D32")

    class_box((3.6, 3.0), 3.0, 1.6, "edge_detection",
               [], ["detect_edges", "clean_edges", "edge_pipeline"], fc="#DFF5DF", ec="#2E7D32")

    class_box((6.9, 3.0), 3.0, 1.6, "segmentation",
               [], ["find_contours", "build_detected_objects", "segmentation_pipeline"], fc="#DFF5DF", ec="#2E7D32")

    class_box((10.1, 3.0), 2.7, 1.3, "shape_classifier",
               [], ["classify_shape", "classify_size", "classify_objects"], fc="#DFF5DF", ec="#2E7D32")

    class_box((0.3, 0.6), 3.0, 1.4, "annotator",
               [], ["annotate_image"], fc="#FDE0E0", ec="#B22222")

    class_box((3.6, 0.6), 3.4, 1.6, "reporting",
               [], ["write_csv_report", "build_summary", "print_summary"], fc="#FDE0E0", ec="#B22222")

    class_box((7.3, 0.6), 3.0, 1.4, "validation",
               [], ["validate_image_path", "validate_output_dir"], fc="#FDE0E0", ec="#B22222")

    class_box((10.6, 0.6), 2.2, 1.4, "main (CLI)",
               [], ["parse_args", "run_pipeline"], fc="#FFF3D6", ec="#B8860B")

    # relationships
    arrow(ax, (10.6, 1.3), (7.5, 1.5), color="#555555")
    arrow(ax, (10.6, 1.3), (7.0, 3.6), color="#555555")
    arrow(ax, (10.6, 1.3), (5.1, 3.6), color="#555555")
    arrow(ax, (10.6, 1.3), (1.8, 3.6), color="#555555")
    arrow(ax, (10.6, 1.3), (1.8, 1.3), color="#555555")
    arrow(ax, (10.6, 1.3), (5.3, 1.3), color="#555555")
    ax.text(9.0, 2.4, "orchestrates", fontsize=8, style="italic", color="#555555")

    arrow(ax, (1.8, 3.0), (5.4, 6.9), connectionstyle="arc3,rad=0.25", color="#888888")
    ax.text(2.8, 5.3, "uses", fontsize=8, style="italic", color="#888888")

    arrow(ax, (8.4, 3.0), (5.3, 6.9), connectionstyle="arc3,rad=-0.15", color="#888888")
    ax.text(7.0, 4.6, "produces", fontsize=8, style="italic", color="#888888")

    plt.tight_layout()
    plt.savefig(f"{OUT}/class_diagram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# -----------------------------------------------------------------------
# 5. SEQUENCE DIAGRAM
# -----------------------------------------------------------------------
def sequence_diagram():
    fig, ax = new_fig(13, 8)
    ax.text(6.5, 7.7, "Sequence Diagram — Single Image Processing Run", ha="center", fontsize=13, weight="bold")

    lifelines = ["User", "main.py", "preprocessing", "edge_detection", "segmentation",
                 "shape_classifier", "annotator", "reporting"]
    xs = [0.8 + i * 1.6 for i in range(len(lifelines))]
    top = 7.1
    bottom = 0.4

    for x, name in zip(xs, lifelines):
        ax.add_patch(FancyBboxPatch((x - 0.65, top), 1.3, 0.4, boxstyle="round,pad=0.05",
                                     facecolor="#DCEBFF", edgecolor="#2C5C9C", linewidth=1.2))
        ax.text(x, top + 0.2, name, ha="center", va="center", fontsize=8.2, weight="bold")
        ax.plot([x, x], [top, bottom], color="#999999", linewidth=1.0, linestyle="--")

    messages = [
        (0, 1, "run(--image path)"),
        (1, 2, "preprocess_pipeline()"),
        (2, 1, "return gray/equalized/blurred", True),
        (1, 3, "edge_pipeline(blurred)"),
        (3, 1, "return cleaned_edges", True),
        (1, 4, "segmentation_pipeline(edges)"),
        (4, 1, "return DetectedObject list", True),
        (1, 5, "classify_objects(objects)"),
        (5, 1, "return labeled objects", True),
        (1, 6, "annotate_image(original, objects)"),
        (6, 1, "return annotated image", True),
        (1, 7, "write_csv_report() / build_summary()"),
        (7, 1, "return summary dict", True),
        (1, 0, "display summary + save files"),
    ]

    y = top - 0.5
    step = (y - (bottom + 0.3)) / len(messages)
    for src, dst, label, *rest in messages:
        dashed = bool(rest and rest[0])
        style = "arc3,rad=0.0"
        arr = FancyArrowPatch((xs[src], y), (xs[dst], y),
                               arrowstyle="-|>", mutation_scale=13,
                               color="#333333", linewidth=1.2,
                               linestyle="dashed" if dashed else "solid",
                               connectionstyle=style)
        ax.add_patch(arr)
        mx = (xs[src] + xs[dst]) / 2
        ax.text(mx, y + 0.12, label, ha="center", fontsize=7.3, color="#333333")
        y -= step

    plt.tight_layout()
    plt.savefig(f"{OUT}/sequence_diagram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    system_architecture()
    workflow_diagram()
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    print("All diagrams generated in", OUT)
