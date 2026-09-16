"""Unit tests for modules.segmentation"""

import os
import sys
import unittest
import numpy as np
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.segmentation import find_contours, build_detected_objects, segmentation_pipeline
from modules.config import DEFAULT_CONFIG


class TestSegmentation(unittest.TestCase):

    def setUp(self):
        # Two clearly separated squares -> two contours
        self.img = np.zeros((200, 200), dtype=np.uint8)
        cv2.rectangle(self.img, (10, 10), (60, 60), 255, -1)
        cv2.rectangle(self.img, (100, 100), (180, 180), 255, -1)

    def test_find_contours_count(self):
        contours = find_contours(self.img)
        self.assertEqual(len(contours), 2)

    def test_build_detected_objects_filters_noise(self):
        contours = find_contours(self.img)
        cfg = DEFAULT_CONFIG
        objects = build_detected_objects(contours, cfg)
        self.assertEqual(len(objects), 2)
        for obj in objects:
            self.assertGreater(obj.area, 0)
            self.assertGreater(obj.perimeter, 0)

    def test_min_area_filter_excludes_small_objects(self):
        contours = find_contours(self.img)
        cfg = DEFAULT_CONFIG
        # force a very high min area -> nothing should survive
        from dataclasses import replace
        strict_cfg = replace(cfg, min_contour_area=1_000_000)
        objects = build_detected_objects(contours, strict_cfg)
        self.assertEqual(len(objects), 0)

    def test_segmentation_pipeline_end_to_end(self):
        objects = segmentation_pipeline(self.img, DEFAULT_CONFIG)
        self.assertEqual(len(objects), 2)
        ids = sorted(o.object_id for o in objects)
        self.assertEqual(ids, [1, 2])


if __name__ == "__main__":
    unittest.main()
