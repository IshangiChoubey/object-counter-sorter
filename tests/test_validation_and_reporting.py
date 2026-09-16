"""Unit tests for modules.validation and modules.reporting"""

import os
import sys
import csv
import shutil
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.validation import (
    validate_image_path, validate_positive_number, validate_output_dir,
    InvalidInputError,
)
from modules.reporting import write_csv_report, build_summary
from modules.segmentation import DetectedObject
import numpy as np


class TestValidation(unittest.TestCase):

    def test_validate_image_path_rejects_missing_file(self):
        with self.assertRaises(InvalidInputError):
            validate_image_path("nonexistent_file.png")

    def test_validate_image_path_rejects_bad_extension(self):
        open("tests/_tmp.txt", "w").close()
        try:
            with self.assertRaises(InvalidInputError):
                validate_image_path("tests/_tmp.txt")
        finally:
            os.remove("tests/_tmp.txt")

    def test_validate_positive_number(self):
        with self.assertRaises(InvalidInputError):
            validate_positive_number(-5, "min_area")
        validate_positive_number(10, "min_area")  # should not raise

    def test_validate_output_dir_creates_directory(self):
        test_dir = "tests/_tmp_output_dir"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        validate_output_dir(test_dir)
        self.assertTrue(os.path.isdir(test_dir))
        shutil.rmtree(test_dir)


class TestReporting(unittest.TestCase):

    def _make_dummy_objects(self):
        objs = []
        for i, (shape, size) in enumerate(
            [("circle", "small"), ("circle", "large"), ("square", "medium")], start=1
        ):
            obj = DetectedObject(
                object_id=i,
                contour=np.array([[[0, 0]], [[1, 0]], [[1, 1]], [[0, 1]]]),
                area=100.0 * i,
                perimeter=40.0,
                bounding_box=(0, 0, 10, 10),
                centroid=(5, 5),
                approx_vertices=4,
                circularity=0.8,
                shape_label=shape,
                size_label=size,
            )
            objs.append(obj)
        return objs

    def test_write_csv_report_row_count(self):
        objs = self._make_dummy_objects()
        out_path = "tests/_tmp_report.csv"
        write_csv_report(objs, out_path)
        with open(out_path) as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 3)
        os.remove(out_path)

    def test_build_summary_counts(self):
        objs = self._make_dummy_objects()
        summary = build_summary(objs)
        self.assertEqual(summary["total_objects"], 3)
        self.assertEqual(summary["by_shape"]["circle"], 2)
        self.assertEqual(summary["by_shape"]["square"], 1)


if __name__ == "__main__":
    unittest.main()
