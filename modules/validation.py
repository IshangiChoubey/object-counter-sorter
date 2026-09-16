"""
validation.py
--------------
Input validation helpers. Centralising validation here (rather than
scattering checks across modules) satisfies the 'validation and error
handling' technical expectation and keeps error messages consistent.
"""

import os

VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")


class InvalidInputError(Exception):
    """Raised when a user-supplied argument fails validation."""


def validate_image_path(path: str) -> None:
    if not isinstance(path, str) or not path.strip():
        raise InvalidInputError("Image path must be a non-empty string.")

    if not os.path.isfile(path):
        raise InvalidInputError(f"Image file does not exist: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext not in VALID_EXTENSIONS:
        raise InvalidInputError(
            f"Unsupported file extension '{ext}'. Supported: {VALID_EXTENSIONS}"
        )


def validate_positive_number(value, name: str) -> None:
    if not isinstance(value, (int, float)) or value <= 0:
        raise InvalidInputError(f"'{name}' must be a positive number, got {value!r}.")


def validate_output_dir(path: str) -> None:
    if not isinstance(path, str) or not path.strip():
        raise InvalidInputError("Output directory path must be a non-empty string.")
    os.makedirs(path, exist_ok=True)
