"""
Utility helpers used across the small modules.
"""
from datetime import datetime
from typing import Union
import os
import tempfile
import shutil
import html


def format_duration(seconds: Union[float, int], absolute: bool = False) -> str:
    """
    Format number of seconds.
    If absolute is True, format as datetime string (used for generated_at).
    """
    try:
        seconds = float(seconds)
    except Exception:
        seconds = 0.0
    if absolute:
        try:
            return datetime.utcfromtimestamp(seconds).isoformat() + "Z"
        except Exception:
            return str(seconds)
    # otherwise human readable like "1.234s"
    try:
        if seconds >= 1.0:
            return "{:.3f}s".format(seconds)
        else:
            return "{:.3f}s".format(seconds)
    except Exception:
        return "{:.3f}s".format(0.0)


def escape_html(s: object) -> str:
    return html.escape("" if s is None else str(s))


def write_file_atomic(path: str, data: bytes) -> None:
    """
    Write bytes to path atomically using a temp file.
    """
    dirpath = os.path.dirname(path) or "."
    fd, temp_path = tempfile.mkstemp(dir=dirpath)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        # use move to replace atomically
        shutil.move(temp_path, path)
    finally:
        # ensure cleanup if something went wrong and file still exists
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass