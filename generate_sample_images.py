"""
generate_sample_images.py
--------------------------
Generates synthetic test images (shapes of varying type/size, and a
coin-like scattering) so the pipeline can be demonstrated and unit
tested without requiring an external dataset download.

Run once: python generate_sample_images.py
Outputs into sample_images/
"""

import os
import cv2
import numpy as np

OUT_DIR = "sample_images"


def make_mixed_shapes_image(path: str):
    """A white canvas with circles, squares, rectangles, and triangles of varying sizes."""
    img = np.full((500, 700, 3), 255, dtype=np.uint8)

    # Circles (small, medium, large)
    cv2.circle(img, (80, 80), 25, (0, 0, 0), -1)          # small
    cv2.circle(img, (220, 90), 45, (0, 0, 0), -1)         # medium
    cv2.circle(img, (400, 100), 70, (0, 0, 0), -1)        # large

    # Squares
    cv2.rectangle(img, (550, 40), (600, 90), (0, 0, 0), -1)     # small square
    cv2.rectangle(img, (50, 220), (140, 310), (0, 0, 0), -1)    # medium square

    # Rectangles
    cv2.rectangle(img, (200, 230), (340, 290), (0, 0, 0), -1)   # wide rectangle
    cv2.rectangle(img, (420, 200), (470, 340), (0, 0, 0), -1)   # tall rectangle

    # Triangles
    pts1 = np.array([[560, 250], [610, 340], [510, 340]], np.int32)
    cv2.fillPoly(img, [pts1], (0, 0, 0))

    pts2 = np.array([[100, 420], [160, 420], [130, 470]], np.int32)
    cv2.fillPoly(img, [pts2], (0, 0, 0))

    # A pentagon (polygon)
    pts3 = np.array(
        [[300, 380], [340, 410], [325, 460], [275, 460], [260, 410]], np.int32
    )
    cv2.fillPoly(img, [pts3], (0, 0, 0))

    cv2.imwrite(path, img)


def make_coin_like_image(path: str):
    """Simulates coins of two denominations scattered on a plain background,
    with soft shading, to better resemble a real photographed scene."""
    rng = np.random.default_rng(42)
    img = np.full((480, 640, 3), 235, dtype=np.uint8)

    # subtle background texture/noise for realism
    noise = rng.normal(0, 4, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    coin_specs = [
        # (center, radius)
        ((90, 90), 32), ((200, 60), 30), ((320, 100), 33), ((460, 70), 31),
        ((560, 120), 34), ((120, 220), 45), ((260, 230), 47), ((420, 210), 46),
        ((560, 260), 44), ((90, 360), 30), ((230, 380), 32), ((380, 360), 47),
        ((520, 390), 31),
    ]

    for (cx, cy), r in coin_specs:
        cv2.circle(img, (cx, cy), r, (150, 150, 150), -1)
        cv2.circle(img, (cx, cy), r, (90, 90, 90), 2)
        cv2.circle(img, (cx - r // 4, cy - r // 4), r // 3, (180, 180, 180), -1)

    cv2.imwrite(path, img)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    make_mixed_shapes_image(os.path.join(OUT_DIR, "shapes_sample.png"))
    make_coin_like_image(os.path.join(OUT_DIR, "coins_sample.png"))
    print(f"Sample images written to '{OUT_DIR}/'.")


if __name__ == "__main__":
    main()
