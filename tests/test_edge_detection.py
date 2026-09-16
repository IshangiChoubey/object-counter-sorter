"""Unit tests for modules.edge_detection"""

import os
import sys
import unittest
import numpy as np
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.edge_detection import detect_edges, clean_edges, edge_pipeline
from modules.config import DEFAULT_CONFIG


class TestEdgeDetection(unittest.TestCase):

    def setUp(self):
        self.img = np.zeros((100, 100), dtype=np.uint8)
        cv2.rectangle(self.img, (20, 20), (80, 80), 255, -1)

    def test_detect_edges_finds_boundary(self):
        edges = detect_edges(self.img, DEFAULT_CONFIG)
        self.assertEqual(edges.shape, self.img.shape)
        self.assertGreater(np.count_nonzero(edges), 0)

    def test_clean_edges_output_binary(self):
        edges = detect_edges(self.img, DEFAULT_CONFIG)
        cleaned = clean_edges(edges, DEFAULT_CONFIG)
        unique_vals = set(np.unique(cleaned).tolist())
        self.assertTrue(unique_vals.issubset({0, 255}))

    def test_edge_pipeline_keys(self):
        result = edge_pipeline(self.img, DEFAULT_CONFIG)
        self.assertIn("raw_edges", result)
        self.assertIn("cleaned_edges", result)

    def test_blank_image_has_no_edges(self):
        blank = np.zeros((50, 50), dtype=np.uint8)
        edges = detect_edges(blank, DEFAULT_CONFIG)
        self.assertEqual(np.count_nonzero(edges), 0)


if __name__ == "__main__":
    unittest.main()
