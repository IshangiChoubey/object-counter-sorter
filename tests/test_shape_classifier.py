"""Unit tests for modules.shape_classifier"""

import os
import sys
import unittest
import numpy as np
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.segmentation import segmentation_pipeline
from modules.shape_classifier import classify_objects, classify_size
from modules.config import DEFAULT_CONFIG


def _find_objects_from_shape_image():
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.circle(img, (60, 60), 40, 255, -1)                       # circle
    cv2.rectangle(img, (150, 20), (220, 90), 255, -1)             # square-ish
    pts = np.array([[50, 200], [110, 200], [80, 260]], np.int32)  # triangle
    cv2.fillPoly(img, [pts], 255)
    return segmentation_pipeline(img, DEFAULT_CONFIG)


class TestShapeClassifier(unittest.TestCase):

    def setUp(self):
        self.objects = _find_objects_from_shape_image()
        self.classified = classify_objects(self.objects, DEFAULT_CONFIG)

    def test_all_objects_get_a_shape_label(self):
        for obj in self.classified:
            self.assertNotEqual(obj.shape_label, "unclassified")

    def test_circle_is_detected(self):
        labels = [obj.shape_label for obj in self.classified]
        self.assertIn("circle", labels)

    def test_triangle_is_detected(self):
        labels = [obj.shape_label for obj in self.classified]
        self.assertIn("triangle", labels)

    def test_square_or_rectangle_is_detected(self):
        labels = [obj.shape_label for obj in self.classified]
        self.assertTrue("square" in labels or "rectangle" in labels)

    def test_size_bucketing_boundaries(self):
        class DummyObj:
            pass
        small = DummyObj(); small.area = 100
        medium = DummyObj(); medium.area = 3000
        large = DummyObj(); large.area = 50000

        self.assertEqual(classify_size(small, DEFAULT_CONFIG), "small")
        self.assertEqual(classify_size(medium, DEFAULT_CONFIG), "medium")
        self.assertEqual(classify_size(large, DEFAULT_CONFIG), "large")


if __name__ == "__main__":
    unittest.main()
