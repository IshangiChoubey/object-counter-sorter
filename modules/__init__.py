"""
Edge/Contour-Based Object Counter & Sorter — core package.

Sub-modules:
    config           - tunable pipeline parameters
    logger_utils     - shared logging setup
    validation       - input validation & custom exceptions
    preprocessing    - grayscale, histogram equalization, blurring
    edge_detection   - Canny edge detection + morphological clean-up
    segmentation     - contour extraction & geometric descriptors
    shape_classifier - shape and size classification
    annotator        - draws results back onto the image
    reporting        - CSV export and summary statistics
"""
