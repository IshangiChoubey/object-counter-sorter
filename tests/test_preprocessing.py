"""Unit tests for modules.preprocessing"""

import os
import sys
import unittest
import numpy as np
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.preprocessing import (
    load_image, to_grayscale, equalize_histogram, denoise_and_smooth,
    preprocess_pipeline, ImageLoadError,
)
from modules.config import DEFAULT_CONFIG


class TestPreprocessing(unittest.TestCase):

    TEST_IMG_PATH = "tests/_tmp_test_image.png"

    @classmethod
    def setUpClass(cls):
        # A tiny synthetic BGR image for fast, deterministic tests
        img = np.zeros((50, 50, 3), dtype=np.uint8)
        cv2.circle(img, (25, 25), 15, (255, 255, 255), -1)
        cv2.imwrite(cls.TEST_IMG_PATH, img)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.TEST_IMG_PATH):
            os.remove(cls.TEST_IMG_PATH)

    def test_load_image_success(self):
        img = load_image(self.TEST_IMG_PATH)
        self.assertEqual(img.shape, (50, 50, 3))

    def test_load_image_missing_file_raises(self):
        with self.assertRaises(ImageLoadError):
            load_image("tests/does_not_exist.png")

    def test_to_grayscale_shape(self):
        img = load_image(self.TEST_IMG_PATH)
        gray = to_grayscale(img)
        self.assertEqual(gray.shape, (50, 50))

    def test_equalize_histogram_output_type(self):
        img = load_image(self.TEST_IMG_PATH)
        gray = to_grayscale(img)
        equalized = equalize_histogram(gray)
        self.assertEqual(equalized.dtype, gray.dtype)
        self.assertEqual(equalized.shape, gray.shape)

    def test_denoise_and_smooth_reduces_noise(self):
        noisy = np.random.randint(0, 255, (50, 50), dtype=np.uint8)
        smoothed = denoise_and_smooth(noisy, DEFAULT_CONFIG)
        # Variance of a blurred image should be lower than pure random noise
        self.assertLess(np.var(smoothed.astype(float)), np.var(noisy.astype(float)))

    def test_preprocess_pipeline_keys(self):
        result = preprocess_pipeline(self.TEST_IMG_PATH, DEFAULT_CONFIG)
        for key in ("original", "gray", "equalized", "blurred"):
            self.assertIn(key, result)


if __name__ == "__main__":
    unittest.main()
